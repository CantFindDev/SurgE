<div align="center">
   <img src="https://i.imgur.com/c6vwoIH.png" alt="Logo"  width=100% height=100%/>
</div>

##

### [Add The Bot To Your Server](https://top.gg/bot/1275846736803401760)

This Discord bot is designed to simulate Growtopia's surgery system, providing an interactive way to learn and practice surgery without the need for in-game tools, world locks, or waiting hours for malpractice. The bot features two distinct modes:

## SurgE Mode

SurgE Mode offers a casual environment where you can practice and reinforce your existing knowledge of surgery techniques. It's a great way to familiarize yourself with the surgery system at your own pace.

## TrainE Mode

TrainE Mode is more structured and educational. In this mode, the bot will provide suggestions based on the specific situation you are in. This helps you understand and learn the appropriate actions for various surgical scenarios, enhancing your overall skillset.

# How to Use

To get started with the bot, use the following commands to simulate the Growtopia surgery system:

## Start a surgery

Generates a random malady with a special condition and set the skill level to 100:

```
/surg
```
## Repeat last command

Repeates the last surgery command with parameters

```
/repeat
```

## Adjust Skill Level

Set your skill level to any value between 0 and 100:

```
/surg skill_level:[SKILL_LEVEL]
```

## Enable Surgery UI with Colors

Activate a surgery UI that mimics the Growtopia surgery simulator with colors:

```
/surg colored_ui:True
```

<img src="https://i.imgur.com/HBqCved.png" width=50% height=50%>

## Select a Specific Modifier

Choose from a list of available modifiers to make surgery easier:

```
/surg modifier:[MODIFIER_NAME]
```

<img src="https://i.imgur.com/guvFOEU.png" width=50% height=50%>

## Select a Specific Malady

Choose from a list of available maladies to practice with:

```
/surg malady:[MALADY_NAME]
```

<img src="ttps://i.imgur.com/AUiMurf.png" width=50% height=50%>

## Activate TrainE Mode

Enable TrainE mode to receive tips and suggestions based on your situation:

```
/surg traine_mode:True
```

<img src="https://i.imgur.com/2UnqmsA.png" width=50% height=50%>

## Enable Ephemeral Embeds

Configure the bot to send ephemeral embedded messages:

```
/surg hidden_embed:True
```

<img src="https://i.imgur.com/JZc7AQM.png" width=50% height=50%>

## Set Special Condition

Customize the special condition of the patient:

```
/surg special_condition:[CONDITION_NAME]
```

<img src="https://i.imgur.com/Gop9wXV.png" width=50% height=50%>

## How to Use the Source Code

### Prerequisites

Ensure that Python 3.12 or later is installed on your device. If not, you can download it from [Python's official website](https://www.python.org/downloads/).

### Cloning the Repository

Clone the source code repository to your local machine using the following command:

```bash
git clone https://github.com/CantFindDev/SurgE.git
```

<img src="https://i.imgur.com/hbpQ6Dp.png" width=50% height=50%>

or you can use in built visual studio code import from git option

<img src="https://i.imgur.com/SB6O6E6.png" width=50% height=50%>

<img src="https://i.imgur.com/0FjbyZl.png" width=50% height=50%>

### Opening the Project

Open the source code in [Visual Studio Code](https://code.visualstudio.com):

The following files are essential once you open the project:

<img src="https://i.imgur.com/FcwE9U8.png" width=25% height=25%>

### Creating a Discord Bot

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "Create Application":

   <img src="https://i.imgur.com/BOQkEv9.png" width=25% height=25%>

3. Configure your application:

   <img src="https://i.imgur.com/M7o2OrD.png" width=50% height=50%>

4. Go to the "Emojis" tab:

   <img src="https://i.imgur.com/n1RBQD9.png" width=50% height=50%>

   Click on "Upload Emojis" and navigate to the project directory to add emojis:

   <img src="https://i.imgur.com/CDcSILN.png" width=50% height=50%>

   Next, open `surg.py` in Visual Studio Code and locate the `ToolIcons` class:

   <img src="https://i.imgur.com/5XOc5uo.png" width=50% height=50%>

   Copy each emoji ID and paste them into the emoji ID section as shown below:

   <img src="https://i.imgur.com/Wh5JesV.png" width=50% height=50%>
   <img src="https://i.imgur.com/w6jjT9x.png" width=50% height=50%>

5. Go back to the "Bot" section:

   <img src="https://i.imgur.com/VhUUk8V.png" width=50% height=50%>

6. Scroll down and enable all **Privileged Gateway Intents**:

   <img src="https://i.imgur.com/PN8FVGs.gif" width=50% height=50%>

7. At the top of the page, click "Reset Token" to copy your bot token (ensure you keep this token confidential):

   <img src="https://i.imgur.com/CaCziMe.png" width=50% height=50%>

### Configuring the Bot
1. Return to your local project directory. And make sure you have Python3 installed
2. Open cmd and type
   ```
   py -3 -m pip install python-dotenv
   py -3 -m pip install -U discord.py
   py -3 -m pip install audioop-lts
   ```
   <img src="https://i.imgur.com/UI1EXwF.png" width=50% height=50%>
   
3. Rename the `EMPTY_.env` file to `.env`:
   
   <img src="https://i.imgur.com/8eHyCho.png" width=25% height=25%>

5. Paste your bot token into the `.env` file as shown below:

   <img src="https://i.imgur.com/rAn5f3Z.png" width=50% height=50%>

### Running the Bot

1. Open a new terminal in Visual Studio Code:

   <img src="https://i.imgur.com/uQcK0uF.png" width=50% height=50%>

1. Execute the following command:

   ```bash
   python Bot.py
   ```
   <img src="https://i.imgur.com/aB1lgyu.png" width=50% height=50%>

2. Wait for the "synced commands" message:

   <img src="https://i.imgur.com/G0cLw1A.png" width=50% height=50%>

### Adding the Bot to Your Server

1. Go back to the Discord Developer Portal and navigate to the "OAuth2" section:

   <img src="https://i.imgur.com/SxPutnw.png" width=25% height=25%>

1. Enable `applications.commands` and select the `Administrator` scope. Scroll down and copy the bot invite link:

   <img src="https://i.imgur.com/pElJf4A.gif" width=50% height=50%>

2. Open the invite link in your browser to add the bot to your server:

   <img src="https://i.imgur.com/ygClVmj.png" width=50% height=50%>

---

Enjoy using your bot! Remember to continue coding and stay curious. If you have any questions or run into issues, feel free to reach out.

# My Socials

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="30" alt="python logo"  />
  <img width="12" />
</div>

<div align="left">
  <a href="https://www.youtube.com/@TheRealCantFind" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Youtube&logo=youtube&label=&color=FF0000&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="youtube logo"  />
  </a>
  <a href="https://discord.gg/kBzFR6Gw2N" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Discord&logo=discord&label=&color=7289DA&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="discord logo"  />
  </a>
</div>

[![MIT License](https://img.shields.io/badge/CantFind-SurgE-red)](https://choosealicense.com/licenses/mit/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
