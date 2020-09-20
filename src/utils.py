from config import TEAMS

def strip_prefix(mes):
    return mes[1:]

def get_command(mes):
    words = mes.split()
    return words[0]

def remove_command(mes):
    first = mes.split()[0]
    start = len(first) + 1
    return mes[start:]

def requires_captain(func):
    async def wrapper(*args, **kwargs):
        message = args[-1]
        captains = [x['captain'] for x in TEAMS]
        roles = [x for x in message.author.roles if x.id in captains]
        if len(roles) == 0:
            return None

        return await func(*args, **kwargs)
    return wrapper
