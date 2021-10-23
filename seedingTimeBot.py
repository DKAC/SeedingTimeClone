import requests, json, os, io, discord, logging, re, datetime, pytz
from dotenv import load_dotenv
from discord.ext import tasks
from seedingTimeVars import *
from seedingTimeLogic import probe


########
# init #
########

level = logging.getLevelName(log_level) if log_level != None else logging.WARNING
logging.basicConfig(encoding='utf-8', level=logging.INFO)
log = io.StringIO()
logging.getLogger().addHandler(logging.StreamHandler(stream=log))


logging.info(f"SeedingTime initializing... {__name__}")

discordClient = discord.Client()
tz = pytz.timezone(timezone)
iteration = 0


###################
# handle messages #
###################

@discordClient.event
async def on_message(msg):
    if (isinstance(msg.channel, discord.channel.DMChannel) or msg.channel.id == discord_channel) and msg.author != discordClient.user:
        cmd, *args = msg.content.split(" ")
        cmd = cmd.lower()
        
        if cmd == "seeding":
            await probe(msg.channel, direct_message=True)
            
        elif cmd == "config": 
            # only 25 values per embed, split vars in batches of 24 (values can be layed out in 3 columns)
            varNames = list(vars.keys())
            for messageNr in range(0, int((len(vars) + 1) / 24) + 1):
                embed=discord.Embed()
                for varNr in range(messageNr * 24, min((messageNr + 1) * 24, len(vars)) - 1): 
                    name = varNames[varNr]
                    embed.add_field(name=name, value=print_env(name))
                await msg.channel.send(embed=embed)
            
        elif cmd == "log":
            tail = 20 
            if len(args) >= 1:
                try:
                    tail = int(args[0])
                except:
                    tail = 20

            lines = log.getvalue().split("\n")
            first_line = 0 if len(lines) <= tail else len(lines) - tail
            for line in lines[first_line:]:
                if line == '': line = '`'
                for part in (line[0+i:4000+i] for i in range(0, len(line), 4000)): # split line into chunks of length 4000
                    await msg.channel.send(content=part)

        elif cmd == "loglevel":
            if len(args) >= 1:
                previousLevel = logging.getLogger().level
                logging.getLogger().setLevel(logging.INFO)
                logging.info(f'Setting log level to {args[0]}')
                try:
                    level = logging.getLevelName(args[0])
                    logging.getLogger().setLevel(level)
                except:
                    logging.info(f'Invalid log level! Reverting to log level {logging._levelToName[previousLevel]}.')
                    level = logging.getLevelName(previousLevel)
                    logging.getLogger().setLevel(level)
            else:
                await msg.channel.send("Usage:\n- loglevel [ERROR|WARNING|INFO|DEBUG]")
        
        elif cmd.lower() == "help":
            await msg.channel.send("\n".join([
                "Usage:", 
                "- seeding", 
                "- config", 
                "- log", 
                "- loglevel"
            ]))


########################
# update in background #
########################

@tasks.loop(minutes=discord_loop_delay)
async def loop():
    global iteration

    channel = discordClient.get_channel(discord_channel)
    if channel == None:
        logging.warning(f"No channel found with id: {discord_channel}")
        iteration = 0
        return

    delay = discord_loop_delay_slow / discord_loop_delay if int(datetime.datetime.now(tz=tz).strftime("%H%M")) < slow_until or channel.name == '🆙-server-up' else 1 # server already up or slow time of day
    if iteration >= delay: iteration = 0
    if iteration > 0:
        logging.info(f"Slow time of day or server already up... wait another {int(discord_loop_delay * (delay - iteration))} minutes")
    
    else:
        await probe(channel)

    iteration += 1


@discordClient.event
async def on_ready():
    if len(discordClient.guilds) > 0: logging.info(f'connected to discord: {discordClient.guilds[0].name}')
    logging.info(f'setting log level to {logging._levelToName[level]} (by environment variable)...')
    logging.getLogger().setLevel(level)
    if discord_loop_delay > 0: 
        loop.start()
    else:
        logging.warning(f"DISCORD_LOOP_DELAY: {discord_loop_delay} => do NOT run in background")


########
# main #
########

logging.info("starting bot...")
discordClient.run(discord_token)
