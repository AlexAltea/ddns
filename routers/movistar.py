import io
import pandas
import re
import requests
import hashlib

def get_public_ip(host, password, **kwargs):
    """
    Obtain public IP address from Movistar routers.
    """
    base = f'http://{host}/cgi-bin'

    # Obtain SID from router
    response = requests.get(f'{base}/logIn_mhs.cgi')
    if response.status_code != 200:
        raise Exception("Could not connect to login page")
    pattern = r'var sid = \'([0-9A-Fa-f]{8})\';'
    match = re.search(pattern, response.text)
    if not match:
        raise Exception("Could not find SID in login page")
    sid = match.group(1)

    # Authenticate into router
    hash = hashlib.md5(f'{password}:{sid}'.encode('utf-8')).hexdigest()
    response = requests.post(f'{base}/logIn_mhs.cgi',
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' },
        data = { 'submitValue': '1', 'syspasswd': hash }
    )
    if response.status_code != 200:
        raise Exception("Could not submit authentication request")
    if 'COOKIE_SESSION_KEY' not in response.cookies:
        raise Exception("Could not authenticate into router. Wrong password?")

    # Get public IP from GPON Connections Table
    response = requests.get(f'{base}/broadband_list.cgi', cookies=response.cookies)
    if response.status_code != 200:
        raise Exception("Could not obtain GPON Connections Table")
    df = pandas.read_html(io.StringIO(response.text), header=0)[0]
    ip = df.query(f"Name == 'Internet'")['IP'].item()
    return ip
