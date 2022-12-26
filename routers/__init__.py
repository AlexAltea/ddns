from . import movistar

def get_public_ip(type, host, username, password):
    if type == "movistar":
        return movistar.get_public_ip(host, password)
    else:
        raise Exception("Unknown router")
