import os, dotenv, json

vars = {}

def get_env(name, default, convert = None, secret = False):
    value = os.environ.get(name, default)
    if convert != None: value = convert(value)
    vars[name] = { "value": value, "secret": secret }
    return value

def print_env(name): 
    if vars[name]['secret']: 
        return '*SECRET*'
    if vars[name]['value'] == None or vars[name]['value'] == '':
        return '*none*'
    else:
        return vars[name]['value']

dotenv.load_dotenv()

own_server_name = get_env('OWN_SERVER_NAME', 'Stoßtrupp Donnerbalken')
match_name = get_env('MATCH_NAME', 'ger')
exclude_names = get_env('EXCLUDE_NAMES', '["event", "geronimo"]', json.loads)
min_players = get_env('MIN_PLAYERS', '2', int)
seeding_players = get_env('SEEDING_PLAYERS', '5', int)
seeded_players = get_env('SEEDED_PLAYERS', '50', int)
full_players = get_env('FULL_PLAYERS', '95', int)
server_part_length = get_env("PART_LENGTH", '30', int)
server_part_lines = get_env("PART_LINES", '2', int)
steam_url = get_env('STEAM_URL', 'https://api.steampowered.com/IGameServersService/GetServerList/v1/')
steam_appid = get_env('STEAM_APPID', '686810')
steam_key = get_env('STEAM_KEY', None, secret=True)
discord_token = get_env('DISCORD_TOKEN', None, secret=True)
discord_channel = get_env('DISCORD_CHANNEL', '0', int)
discord_notification_role = get_env('DISCORD_NOTIFICATION_ROLE', None)
discord_loop_delay = get_env('DISCORD_LOOP_DELAY', '2', int)
discord_loop_delay_slow = get_env('DISCORD_LOOP_DELAY_SLOW', '10', int)
slow_until = get_env('SLOW_UNTIL', '1200', int)
timezone = get_env("TIMEZONE", "Europe/Berlin")
log_level = get_env('LOG_LEVEL', "WARNING")

msg_seeding_time = { 
    'channel_name': get_env('MSG_SEEDING_TIME_CHANNEL_NAME', '🌱-seeding-time'),
    'title':        get_env('MSG_SEEDING_TIME_TITLE',        'SEEDING TIME!'), 
    'description':  get_env('MSG_SEEDING_TIME_DESCRIPTION',  'Keine "{match_name}" Server mit {seeding_players} bis {full_players} Spielern gefunden...')
}

msg_no_seeding = { 
    'channel_name': get_env('MSG_NO_SEEDING_CHANNEL_NAME', '😴-kein-seeding'),
    'title':        get_env('MSG_NO_SEEDING_TITLE',        'Seeding lohnt sich noch nicht...'), 
    'description':  get_env('MSG_NO_SEEDING_DESCRIPTION',  '{servers} "{match_name}" Server mit {seeding_players} bis {full_players} Spielern gefunden...')
}

msg_server_up = {
    'channel_name': get_env('MSG_SERVER_UP_CHANNEL_NAME', '🆙-server-up'),
    'title':        get_env('MSG_SERVER_UP_TITLE',        'Server ist geseeded'),
    'description':  get_env('MSG_SERVER_UP_DESCRIPTION',  'Lasst ihn nicht sterben...')
}

msg_seeding_in_progress = {
    'channel_name': get_env('MSG_SERVER_UP_CHANNEL_NAME', '🌱-seeding-läuft'),
    'title':        get_env('MSG_SERVER_UP_TITLE',        'SEEDING TIME!'),
    'description':  get_env('MSG_SERVER_UP_DESCRIPTION',  'User Server wird gerade geseeded... hilf mit!')
}


