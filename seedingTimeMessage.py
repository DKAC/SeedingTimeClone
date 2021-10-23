import logging, datetime, pytz, discord
from seedingTimeVars import *

discord_message = None
tz = pytz.timezone(timezone)


async def purge(channel):
    if discord_message != None: await channel.purge(check=lambda msg: msg.id != discord_message)
    

async def send(msg_vars, channel, servers, notification_role, direct_message):
    channel_name = msg_vars['channel_name']
    
    title = msg_vars['title']
    
    description = msg_vars['description'].format(
        servers=len(servers), 
        match_name=match_name, 
        seeding_players=seeding_players, 
        full_players=full_players
    )
    
    await sendMessage(channel, channel_name, title, description, servers, notification_role, direct_message)


async def sendMessage(channel, channel_name, title, description, servers, notification_role, direct_message):
    global discord_message

    # check if message exists

    # todo how to find the message after restarting the bot
    if discord_message != None and direct_message == False:
        try:
            msg = await channel.fetch_message(discord_message)
            discord_message = msg.id
        except:
            logging.warning(f"message not found: {discord_message}")
            discord_message = None
    
    # build description from server list
    s = ""
    if servers != None and len(servers) > 0:
        for server in servers:
            t = ""
            for part in (server.name[0+i:server_part_length+i] for i in range(0, min(server_part_lines * server_part_length, len(server.name)), server_part_length)): # split line into chunks
                if t == "":
                    t += f"{server.players:>3} - {part}\n"
                else:
                    t += f"      {part}\n"
            s += t
        
        description += "\n```" + s + "```"

    # build dicord embed
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text=f"Updated: {datetime.datetime.now(tz=tz).strftime('%d.%m.%y %H:%M:%S')}")
    
    logging.info(f"message: {title}, {description}")
    
    if notification_role != None and notification_role != '': notification_role = f'@{notification_role}'
    
    # send message
    if direct_message == True:
        await channel.send(embed=embed)
        logging.info(f"direct message sent...")
        
    elif discord_message == None:
        msg = await channel.send(embed=embed, content=notification_role)
        discord_message = msg.id
        logging.info(f"message created: {discord_message}")
        
    else:        
        await msg.edit(embed=embed, content=notification_role)
        logging.info(f"message updated: {discord_message}")
    
    # update channel name
    if direct_message == False and channel_name != channel.name:
        logging.info(f'Changing channel name from "{channel.name}" to "{channel_name} (if rate limited, it may take quite a while to update)"')
        await channel.edit(name=channel_name)
        logging.info(f'Channel name changed from "{channel.name}" to "{channel_name}"')