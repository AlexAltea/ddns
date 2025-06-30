from . import movistar
from . import turris

def get_public_ip(type, host, username, password):
    if type == "movistar":
        return movistar.get_public_ip(host, password)
    elif type == "turris":
        return turris.get_public_ip(host, username, password)
    else:
        raise Exception("Unknown router")
