"""
Upload through SSH
"""
import logging
import os
from paramiko import SSHClient, AutoAddPolicy


logger = logging.getLogger(__name__)


def upload_ssh(stream_path,
               host,
               user,
               password,
               destination_folder,
               port=22,
               delete_on_success=False):

    """ Upload with SSH """
    # TODO allow use keys instead user/pass
    logging.info(f'Uploading {stream_path}')

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(host, port, user, password)

    sftp = ssh.open_sftp()

    filename = stream_path.split('/')[-1]
    destination_path = os.path.join(destination_folder, filename)
    logging.info(f'Copying from {stream_path} to {destination_path}')
    sftp.put(localpath=stream_path, remotepath=destination_path)

    sftp.close()
    ssh.close()

    if delete_on_success:
        logging.info(f'Deleting {stream_path}')
        os.remove(stream_path)
    else:
        return stream_path
