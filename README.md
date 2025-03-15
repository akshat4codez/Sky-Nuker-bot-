# Discord Nuker Bot 

A powerful Discord bot for server management, capable of executing various commands such as channel creation, deletion, mass pings, invite spamming, and more. This bot is intended for use in testing environments or private servers only. Please use responsibly.

---

## Features

- **Channel Creation**: Create multiple text and voice channels in bulk.
- **Channel Deletion**: Delete all channels in the server.
- **Mass Ping**: Send a mass ping message to all members of the server.
- **Invite Spam**: Spam invite links in all text channels.
- **Role Deletion**: Delete all roles in the server.
- **Ban All**: Ban all members from the server.
- **Send Custom Messages**: Send messages to specific channels or all channels.
- **Rate Limiting**: Automatic handling of Discord's rate limiting.
- **Bot Info**: Fetch bot information including its username and prefix.

---

## Requirements

- **Python** 3.7 or higher (only for development)
- **aiohttp** library (for asynchronous HTTP requests)
- **Config.json** for bot configuration settings (includes `TOKEN`, `guild_id`, etc.)

---

## How to Use

1. **Install Dependencies** (if you are running the script directly):
    - Install Python 3.7 or higher.
    - Install the necessary libraries:
      ```bash
      pip install aiohttp
      ```

2. **Configure the Bot**:
   - Edit the `config.json` file to include your bot's token, guild ID, and prefix.
   - ![image](https://github.com/user-attachments/assets/49f23bd0-ca77-4da0-bd8d-05be6ef6d862)


3. **Interact with the Bot**:
   - Upon launching, the bot will show a menu.
   - Use the options in the menu to:
     - Fetch bot information.
     - Send messages to channels.
     - Create or delete channels.
     - Ban all members.
     - Spam invites and perform mass pings.
     - Ping @everyone in all channels while creating channels
     - Delete role in server
       
---

## Example Command Flow

Upon running the bot, a menu will be displayed. Example:
![image](https://github.com/user-attachments/assets/657a20ef-ce10-4bf9-aba4-97a28b41a489)





