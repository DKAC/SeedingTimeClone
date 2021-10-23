import logging, requests, types
from seedingTimeVars import *
from seedingTimeMessage import send, purge

own_players = None

async def probe(channel, direct_message = False):
    global own_players
    logging.info(f'{channel}') 

    request = requests.get(steam_url, params={'key':steam_key, 'filter':f'\\appid\\{steam_appid}\\name_match\\*{match_name}*'})

    if request.status_code == 200:
        body = json.loads(request.text, object_hook=lambda d: types.SimpleNamespace(**d))
        # get list of servers with at least min_players that do not match any term in the exclude list, sorted by players (descending)
        servers = [server for server in body.response.servers 
                   if ( server.players >= min_players ) 
                   and next((False for name in exclude_names if name.upper() in server.name.upper()), True)] 
        servers.sort(key=lambda server: server.players, reverse=True)

        # get list of servers with players within [seeding_players, full_players]
        seeding = [server for server in servers if ( server.players >= seeding_players ) and ( server.players < full_players )]

        # check if own server is up or seeding is in progress
        for own in [server for server in servers if own_server_name.upper() in server.name.upper()]:
            if own_players != None: logging.info(f"previous own_players: {own_players}")
            # to deal with short term changes in player counts, take history into account
            own_players = own.players if own_players == None else int((own_players + own.players) / 2)
            logging.info(f"current players: {own.players} => new own_players: {own_players}")
            
            if own_players >= seeded_players:
                await send(msg_server_up, channel, [own], None, direct_message)
                return
            
            if own_players > seeding_players and own_players < seeded_players:
                await send(msg_seeding_in_progress, channel, seeding, discord_notification_role, direct_message)
                return

        # check if it's seeding time or other servers are being seeded already
        if len(seeding) == 0:
            await send(msg_seeding_time, channel, servers, discord_notification_role, direct_message)
        else:
            await send(msg_no_seeding, channel, seeding, None, direct_message)
            
    else:
        logging.warning(f'Steam request failed: {request.status_code}')

    # remove other messages than the seeding info message
    if direct_message == False: 
        await purge(channel)
