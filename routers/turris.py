import logging
import paramiko

def get_public_ip(host, username, password):
    command = "/sbin/ifconfig pppoe-wan | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1 }'"
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        client.close()

        if error:
            logging.error(f"Error running command: {error}")
            return None

        return output

    except Exception as e:
        logging.error(f"SSH connection or command failed: {e}")
        return None
