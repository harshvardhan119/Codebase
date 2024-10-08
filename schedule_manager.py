from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Request
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from gpt_worker import get_full_text_string, process_using_gemini
from email_send import send_email
import pymongo
import threading
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize a WebClient instance with your OAuth token
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)
app = FastAPI()


mongodb_uri = os.getenv("MONGODB_URL")

# Connect to MongoDB
client = pymongo.MongoClient(mongodb_uri)
db = client["Cluster0"]
collection = db["workflows"]

# Create a lock to synchronize access to shared resources
lock = threading.Lock()


# init the scheduler
scheduler = BackgroundScheduler()



# list of dictionary contains user details
user_dict = []
# This list contains all the jobs ids
list_ids = []

# this function store workflow details in mongodb
async def add_workflow_to_db(data):

    workflowTime = data["workflowTime"]
    hour, minute = map(int, workflowTime.split(':'))
    workflowId = str(uuid.uuid4())

    # Define a document to insert
    data = {
        "userid" : data["userid"],
        "workflowName" : data["workflowName"],
        "senderChannelId" : data["senderChannelId"],
        "receiverChannelId" : data["receiverChannelId"],
        "prompt" : data["prompt"],
        "timeperiod" : data["timeperiod"],
        "hour":hour,
        "minute":minute,
        "pastChatHours" : data["pastChatHours"],
        "receiverChannelName" : data["receiver_channel_name"],
        "senderChannelName" : data["sender_channel_name"],
        "jobids":list_ids,
        "workflowid": workflowId
    }

    try:
        # Insert the document into the MongoDB collection
        result = collection.insert_one(data)
        list_ids.clear()
        return {"message": "Document inserted successfully", "document_id": str(result.inserted_id)}
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")





# Function to get members details of a Slack channel and their timezones
async def get_channel_members_with_timezones(channel_id):
    try:
        # Call the users.list API method to retrieve members of the channel
        response = slack_client.conversations_members(channel=channel_id)

        members = response['members']

        for member_id in members:
            try:
                # Call the users.info method using the WebClient
                result = slack_client.users_info(
                    user=member_id
                )
                timezone = result["user"].get("tz")
                email = result["user"]["profile"].get("email")
                name = result["user"]["profile"].get("real_name")

                if email and timezone and name:
                    user_obj = {
                        "user_email":email,
                        "name":name,
                        "timezone":timezone,
                        "userid":member_id
                    }
                    user_dict.append(user_obj)
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))
        return user_dict
    except SlackApiError as e:
        print(f"Error: {e}")



# Define a function to send messages
def send_messages_to_channel(user_id, email, name, senderChannel, senderChannelId, pastChatHours, prompt):

    with lock:

        # get the response from GPT Model
        full_messages_string = get_full_text_string(senderChannelId, pastChatHours)
        responseText = process_using_gemini(full_messages_string, prompt)
        print(responseText)

        message = f"""
                    Hi *{name}*,
            
                    This is a important message from *{senderChannel}*
            
                    {responseText}
        """

        try:

            # Call the chat.postMessage method to send a direct message
            response = slack_client.chat_postMessage(channel=user_id, text=message, parse="mrkdwn", mrkdwn=True)

            subject = f"ChannelSync Notification from {senderChannel}"

            # send personal emails to users according to their timezones
            send_email(subject, responseText, email, name, senderChannel)

            print("Message sent successfully:", response)

        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")




# Define a function to schedule sending messages at 9 AM in different timezones
@app.post("/schedule_jobs/", status_code=200)
async def schedule_messages(request: Request):
    # get the payload from the request body
    payload = await request.json()

    receiverChannelId = payload["receiverChannelId"]
    senderChannelId = payload["senderChannelId"]
    prompt = payload["prompt"]
    pastChatHours = payload["pastChatHours"]
    timeperiod = payload["timeperiod"]
    workflowTime = payload["workflowTime"]
    senderChannelName = payload["sender_channel_name"]


    h, m = map(int, workflowTime.split(':'))

    print(receiverChannelId, senderChannelId, prompt, pastChatHours, timeperiod, workflowTime, h, m)

    # clear the dictionary to store only the new details and clear the past user details
    user_dict.clear()

    # get all the members of the receiving channel
    await get_channel_members_with_timezones(receiverChannelId)

    print(user_dict)


    # Schedule sending messages for each timezone
    for data in user_dict:
        user_timezone = data.get("timezone")
        tz = timezone(user_timezone)
        userid = data.get("userid")
        user_email = data.get("user_email")
        name = data.get("name")
        job_id = str(uuid.uuid4())
        list_ids.append(job_id)

        # schedule for every day
        if timeperiod == "1D":
            temp_cron = CronTrigger(hour=int(h),
                                    minute=int(m),
                                    timezone=tz)
            scheduler.add_job(send_messages_to_channel, temp_cron, args=[userid, user_email, name, senderChannelName, senderChannelId, pastChatHours, prompt], id=job_id)

        # schedule for every week on sunday
        if timeperiod == "1W":
            temp_cron = CronTrigger(day_of_week=6,
                                    hour=int(h),
                                    minute=int(m),
                                    timezone=tz)
            scheduler.add_job(send_messages_to_channel, temp_cron, args=[userid, user_email, name, senderChannelName, senderChannelId, pastChatHours, prompt], id=job_id)


        # schedule for every month
        if timeperiod == "1M":
            temp_cron = CronTrigger(day=28,
                                    hour=int(h),
                                    minute=int(m),
                                    timezone=tz)

            scheduler.add_job(send_messages_to_channel, temp_cron, args=[userid, user_email, name, senderChannelName, senderChannelId, pastChatHours, prompt], id=job_id)

    # push workflow details to database
    await add_workflow_to_db(payload)

    return {"message": "successfully scheduled the workflow"}



# Endpoint for getting all tasks
@app.get("/get_all_task/", status_code=200)
async def get_all_task():
    try:
        all_job_ids = [job.id for job in scheduler.get_jobs()]

        return {"message": f"all jobs: {all_job_ids}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get all task: {str(e)}")



# Endpoint for removing a specific task using taskIds
@app.post("/remove_task/", status_code=200)
async def remove_task(request: Request):
    data = await request.json()
    print(data)
    try:
        taskIds = data["jobids"]
        # remove the task from the scheduler
        for task_id in taskIds:
            scheduler.remove_job(task_id)

        return {"message": f"Jobs {taskIds} removed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove task {id}: {str(e)}")



if __name__ == "__main__":
    scheduler.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
