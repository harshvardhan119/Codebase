


## 🏗️ System Architecture:


![System Architecture of ChannelSync](https://github.com/karankulshrestha/channelsync/assets/42493387/6cc46f29-40c4-4563-8266-14bae373ad7c)



# ChannelSync

Introducing ChannelSync, the smart Slack bot powered by Gemini AI. It makes syncing conversations between two channels a breeze. No more digging through endless messages! With ChannelSync, you get the most important info without the hassle.

ChannelSync uses advanced AI to summarize conversations, giving you clear, easy-to-understand insights. It saves time and boosts productivity by focusing on what matters most.

Plus, ChannelSync sends notifications to every member of the specific receiving channel, considering their time zones. This keeps teams updated on changes, no matter where they are.

Say hello to ChannelSync: your go-to for better communication, higher productivity, and staying in the loop.



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGODB_URL`

`SLACK_BOT_TOKEN`

`SLACK_APP_TOKEN`

`SLACK_SIGNING_SECRET`

`GEMINI_API_KEY`

`SMTP_SERVER`

`SMTP_USERNAME`

`SMTP_PORT`

`SMTP_PASSWORD`

## Screenshots

![i1](https://github.com/karankulshrestha/channelsync/assets/42493387/3183d4d1-1257-4d11-802e-18a2c46cc4b8)

![i2](https://github.com/karankulshrestha/channelsync/assets/42493387/c8b42305-75ab-4778-acb5-99f39d5e839d)

![i3](https://github.com/karankulshrestha/channelsync/assets/42493387/ae4f1456-020c-4e3b-bd9c-d30f4a68a65b)

![i4](https://github.com/karankulshrestha/channelsync/assets/42493387/86f12b72-b24d-421b-887a-115051a179ee)

![Screenshot 2024-02-16 211732](https://github.com/karankulshrestha/channelsync/assets/42493387/8562c755-63ec-4fe1-8ca9-f55189b69dbb)

![i6](https://github.com/karankulshrestha/channelsync/assets/42493387/d5d1f7f6-b19d-4d32-aca0-437c6823ff35)

![i5](https://github.com/karankulshrestha/channelsync/assets/42493387/b0970b38-8bb2-4892-8187-fbd0a0b6054a)


## Features

- **Automated Workflow Creation**: Easily create workflows to process past chat conversations from one channel to another, like Marketing to Product Team.

- **Custom GPT Prompt Integration**: Utilize custom GPT prompts to generate insightful summaries of conversations tailored to your team's needs.

- **Scheduled Notifications**: Set up automatic schedulers to send processed chat outputs to team members' Slack DMs and emails at specific times, ensuring they stay updated without manual intervention.

- **Global Timezone Handling**: ChannelSync intelligently handles timezones, ensuring notifications are sent at the appropriate times for global team members.

- **Effortless Workflow Management**: Users can easily create, deploy, and delete workflows for syncing channels, streamlining communication between teams.

- **Gemini AI-powered Summaries**: Advanced AI capabilities summarize conversations, providing clear and concise insights without the need to sift through endless messages.

- **Enhanced Productivity**: By focusing on essential information, ChannelSync saves time and boosts productivity, allowing teams to stay informed without distraction.

- **Comprehensive Team Notifications**: Notifications are sent to every member of the receiving channel, keeping everyone in the loop and aligned with the latest updates.

## Run Locally

Clone the project


Go to the project directory

```bash
  cd channelsync
```

Install dependencies

```bash
  pip install -m requirements.txt
```

Enviroment Variables

```bash
  Build new app on Slack and Get the all required 
  enviroment variables and don't forget to integrate 
  the slack app in workspace.
```


Run the API

```bash
  python schedule_manager.py
```

Run the slack app

```bash
  python main.py
```

## Tech Stack

**Development:** Python, FastAPI, Slack Sdk, Block-Kit, MongoDB, Gemini




## Contributing

Contributions are always welcome!

