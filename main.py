# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
import pymongo, requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mongodb_uri = os.getenv("MONGODB_URL")

# Connect to MongoDB
client = pymongo.MongoClient(mongodb_uri)
db = client["Cluster0"]
collection = db["workflows"]

slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
slack_app_token = os.getenv("SLACK_APP_TOKEN")

# Initialize your app with your bot token and signing secret
app = App(
    token=slack_bot_token,
    signing_secret=slack_signing_secret
)

app_token = slack_app_token
callback_id = "home_view"

client = WebClient(token=app_token)

# Design View of the HomeTab of Bot.
home_tab_view = {
    "type": "home",
    "callback_id": "home_view",
    # body of the view
    "blocks": [
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "# 🌟 Welcome to the Atlan's Automation Workflow! 🚀✨"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "block_id": "workflow_input_field",
            "label": {
                "type": "plain_text",
                "text": "WorkFlow Name"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "workflow_field_id",
                "placeholder": {
                    "type": "plain_text",
                    "text": "name"
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "sender_block_id",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a sender channel from the dropdown list"
            },
            "accessory": {
                "action_id": "sender_action_id",
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select sender channel"
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "receiver_block_id",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a receiver channel from the dropdown list"
            },
            "accessory": {
                "action_id": "receiver_action_id",
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select receiver channel"
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "block_id": "text_area_block",
            "label": {
                "type": "plain_text",
                "text": "Enter Your GPT Prompt"
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "text_area_action",
                "multiline": True  # This specifies that it's a multi-line text input
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "interval_id",
            "text": {
                "type": "mrkdwn",
                "text": "Select Workflow Timeperiod! 😊"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select the interval",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1D",
                            "emoji": True
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1W",
                            "emoji": True
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1M",
                            "emoji": True
                        },
                        "value": "value-2"
                    }
                ],
                "action_id": "static_select-action"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "workflowtime_id",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a time for workflow"
            },
            "accessory": {
                "type": "timepicker",
                "action_id": "workflowtime_action_id",
                "initial_time": "11:40",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a time"
                }
            },
        },
        {
            "type": "divider"
        },
        {
        "type": "input",
        "block_id": "past_hours_id",
          "element": {
            "type": "number_input",
            "is_decimal_allowed": False,
            "action_id": "number_input-action"
          },
          "label": {
            "type": "plain_text",
            "text": "Past Chat Hours",
            "emoji": True
          }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Deploy Workflow"
                    },
                    "style": "primary",
                    "action_id": "submit_button_id"
                }
            ]
        }
    ]
}



# Event Trigger on Loading Home Tab
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view=home_tab_view
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")




# Event Trigger when Submit Button Pressed
@app.action("submit_button_id")
def handle_submission(ack, body, client):
    # Acknowledge the receipt of the view submission
    ack()
    user_id = body["user"]["id"]
    submitted_values = body["view"]["state"]["values"]

    workflowName = submitted_values["workflow_input_field"]["workflow_field_id"]["value"]
    senderChannel = submitted_values["sender_block_id"]["sender_action_id"]["selected_channel"]
    receiverChannel = submitted_values["receiver_block_id"]["receiver_action_id"]["selected_channel"]
    prompt = submitted_values["text_area_block"]["text_area_action"]["value"]

    timeperiod = None
    if submitted_values["interval_id"]["static_select-action"]["selected_option"] != None:
        timeperiod = submitted_values["interval_id"]["static_select-action"]["selected_option"]["text"]["text"]

    workflowTime = submitted_values["workflowtime_id"]["workflowtime_action_id"]["selected_time"]

    pastChatHours = submitted_values["past_hours_id"]["number_input-action"].get("value", 0)
    # if submitted_values["past_hours_id"]["number_input-action"] != None:
    #     pastChatHours = submitted_values["past_hours_id"]["number_input-action"].get("value")

    sender_channel_name = None
    receiver_channel_name = None

    try:
        response = client.conversations_info(channel=senderChannel)
        sender_channel_name = response["channel"]["name"]
        print(f"Channel name: {sender_channel_name}")
    except Exception as e:
        print(f"Error retrieving channel info: {e}")


    try:
        response = client.conversations_info(channel=receiverChannel)
        receiver_channel_name = response["channel"]["name"]
        print(f"Channel name: {receiver_channel_name}")
    except Exception as e:
        print(f"Error retrieving channel info: {e}")


    # All Input checks

    if any(val is None for val in [workflowName, senderChannel, receiverChannel,
                                   prompt, timeperiod, workflowTime, pastChatHours,
                                   receiver_channel_name, sender_channel_name]) or int(pastChatHours) <= 0:
        return client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "Error"
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "Error: All values required or past-chat-hours is not negative or 0"
                        }
                    }
                ],
                "close": {
                    "type": "plain_text",
                    "text": "Close"
                }
            }
        )

    workflow_object = {
        "userid":user_id,
        "workflowName":workflowName,
        "senderChannelId":senderChannel,
        "receiverChannelId":receiverChannel,
        "prompt":prompt,
        "timeperiod":timeperiod,
        "workflowTime":workflowTime,
        "pastChatHours":pastChatHours,
        "receiver_channel_name":receiver_channel_name,
        "sender_channel_name":sender_channel_name
    }

    user_id = body["user"]["id"]



    url = "http://127.0.0.1:8001/schedule_jobs/"

    # Make your external API request
    try:
        response = requests.post(url, json=workflow_object)
        try:
            client.chat_postMessage(channel=user_id,
                                    text=f"\n*WorkFlow is deployed successfully*\n ```{workflow_object}``` \n", parse="mrkdwn", mrkdwn=True)
        except Exception as e:
            print(f"Error sending message: {e}")
        print("Request was successful!")
        print("Response:", response.json())
        # Display the successful messages
    except Exception as e:
        error_message = f"An error occurred while processing your request: {str(e)}"
        print(error_message)
        try:
            client.chat_postMessage(channel=user_id,
                                    text=f"\n*WorkFlow is deployment failed*\n ```{error_message}``` \n")
        except Exception as e:
            print(f"Error sending message: {e}")

    print(workflow_object)


# action Trigger when Sender channel selected
@app.action("sender_action_id")
def handle_submission(ack, body, view):
    # Acknowledge the receipt of the view submission
    ack()


# action trigger when receiver channel selected
@app.action("receiver_action_id")
def handle_submission(ack, body, view):
    # Acknowledge the receipt of the view submission
    ack()



# Action dispatch when radio button selected
@app.action("static_select-action")
def handle_radio(ack, body, view):
    # Acknowledge the receipt of the view submission
    ack()



# Action dispatch when workflow time selected
@app.action("workflowtime_action_id")
def handle_time(ack, body, view):
    # Acknowledge the receipt of the view submission
    ack()




def getWorkflows(userid):
    datalist = []
    # Find a document in the collection (you can use any query here)
    document = collection.find({"userid": userid})

    # Retrieve the ObjectId of the document
    for data in document:
        datalist.append(data)
    if len(datalist) > 0:
        return datalist
    else:
        print("Document not found.")




# Command for listing all deployed workflows in message tab.
@app.command("/list-workflows")
def echo_command(ack, say, context):
    # Acknowledge the command
    ack()

    user_id = context["user_id"]

    # List of all deployed workflows
    data = getWorkflows(user_id)

    header = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Workflows",
                "emoji": True
            }
        }
    ]

    say(blocks=header)


    widgets = []

    # formatting the design of each workflow bot and append to blocks list.
    for card in data:
        widgets.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{card['workflowName']}*\n{card['prompt']}*\n{card['senderChannelName']} =====> {card['receiverChannelName']}*\n"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Delete"
                    },
                    "style": "danger",
                    "value": card["workflowid"],
                    "action_id": "delete-btn"
                }
            }
        )

    # Send the message with the card
    if len(widgets) > 0:
        say(blocks=widgets)
    else:
        say("Sorry No, WorksFlow's found!")


# Action dispatch when delete button pressed.
@app.action("delete-btn")
def delete_handle(ack, say, body):
    # Acknowledge the command
    ack()

    Id = body["actions"][0]["value"]

    result = collection.find_one({"workflowid" : Id})
    tasks = {
        "jobids": result["jobids"]
    }

    url = "http://127.0.0.1:8001/remove_task/"

    # Make your external API request
    try:
        response = requests.post(url, json=tasks)
        # Delete the document with the specified UUID
        result = collection.delete_one({"workflowid": Id})
        print("Response:", response.json())
        # Check if the deletion was successful
        if result.deleted_count == 1:
            say("deletion successful")
        else:
            say(f"No workflow with UUID {Id} found.")
    except Exception as e:
        error_message = f"An error occurred while processing your request: {str(e)}"
        print(error_message)




# app for invoking the connection
def run_bot():
  SocketModeHandler(app, app_token).start()


# Ready? Start your app!
if __name__ == "__main__":
    # getWorkflows()
    run_bot()
    # app.start(port=int(os.environ.get("PORT", 3000)))
