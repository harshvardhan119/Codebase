from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
# Initialize a Slack WebClient instance with your bot token
client = WebClient(token=slack_bot_token)

# Define the channel ID where you want to post the message
channel_id = 'C06JK7MFH7D'

# sample testing messages
messages = [" Market Team: Exciting news! We've uncovered a new customer segment with huge potential. ",
 ' Product Team: Great! What are their pain points? ',
 ' Market Team: They need a more efficient way to aggregate and analyze data. ',
 " Product Team: That's perfect! Our new data management software is designed for just that. ",
 " Customer Support Team: We've received a lot of feedback from customers requesting a mobile app. ",
 " Product Team: We'll prioritize developing a mobile app to meet those needs. ",
 ' Market Team: Insights from our latest market survey show a growing demand for personalization. ',
 " Product Team: Thanks for sharing! We'll explore incorporating personalization features into our offerings. ",
 " Market Team: We've identified a competitor gaining market share with a more user-friendly interface. ",
 " Product Team: We'll conduct a UX audit and make improvements to enhance the user experience. ",
 ' Customer Support Team: Some customers have reported difficulties accessing the software on certain browsers. ',
 " Product Team: We'll investigate the issue and release a software update to address it. ",
 " Market Team: We've noticed a decline in customer satisfaction scores. ",
 " Product Team: We'll gather feedback and conduct a root cause analysis to identify areas for improvement. ",
 ' Market Team: Our competitor has launched a new product that seems to be resonating with customers. ',
 " Product Team: We'll analyze their product, identify its strengths, and explore ways to differentiate our offerings. ",
 " Customer Support Team: We've received positive feedback on our recently launched feature. ",
 " Market Team: That's great! We'll promote it further to increase adoption. ",
 ' Market Team: Industry reports predict a shift towards subscription-based services. ',
 " Product Team: We'll evaluate our business model and consider offering a subscription option. ",
 ' Customer Support Team: Some customers have encountered bugs in the latest software update. ',
 " Product Team: We'll roll out a hotfix to resolve the bugs and minimize customer impact. ",
 " Market Team: We've identified a potential partnership with a company that could complement our offerings. ",
 " Product Team: Let's explore the partnership and assess if it aligns with our strategic goals. ",
 " Customer Support Team: We've received a surge in support requests for a particular product feature. ",
 " Product Team: We'll investigate the feature and consider enhancing its functionality or documentation. ",
 ' Market Team: Our competitor has announced a major acquisition that could reshape the market landscape. ',
 " Product Team: We'll conduct a competitive analysis and adjust our strategy accordingly. ",
 " Customer Support Team: We've identified a common customer pain point that could be addressed with a minor software update. ",
 " Product Team: We'll prioritize the update and release it as soon as possible. ",
 " Market Team: We've observed a growing trend towards sustainable products. ",
 " Product Team: We'll explore ways to incorporate sustainability into our product line. ",
 ' Customer Support Team: Some customers have expressed difficulty understanding our pricing model. ',
 " Product Team: We'll review our pricing strategy and make adjustments to improve clarity. ",
 " Market Team: Our competitor has launched a loyalty program that's gaining traction. ",
 " Product Team: We'll evaluate the effectiveness of their program and consider implementing a similar strategy. ",
 " Customer Support Team: We've received feedback that our documentation is difficult to navigate. ",
 " Product Team: We'll redesign the documentation to enhance its usability and accessibility. "]


# Define the message you want to post


def send_to_channel():
    try:
        # Call the chat.postMessage method to post the message to the channel
        for message in messages:
            response = client.chat_postMessage(
                channel=channel_id,
                text=message
            )
        print("Message posted successfully")
    except SlackApiError as e:
        print("Error posting message:", e.response['error'])


send_to_channel()