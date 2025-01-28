#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""
from fabric import task
from datetime import datetime
import os

env.hosts = ['<IP web-01>', 'IP web-02']


@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of web_static folder
    
    Returns:
        str: path to archive if successful, None otherwise
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        
        c.local("tar -cvzf {} web_static".format(archive_path))
        
        return archive_path
    except Exception:
        return None


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to the archive to deploy
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace('.tgz', '')
        remote_path = '/tmp/{}'.format(file_name)
        release_path = '/data/web_static/releases/{}'.format(folder_name)
        
        c.put(archive_path, remote_path)
        c.run('mkdir -p {}'.format(release_path))
        c.run('tar -xzf {} -C {}'.format(remote_path, release_path))
        c.run('rm {}'.format(remote_path))
        c.run('mv {}/web_static/* {}/'.format(release_path, release_path))
        c.run('rm -rf {}/web_static'.format(release_path))
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {} /data/web_static/current'.format(release_path))
        
        print('New version deployed!')
        return True
    except Exception:
        return False


@task
def deploy(c):
    """
    Creates and distributes an archive to web servers
    
    Returns:
        bool: True if successful, False otherwise
    """
    archive_path = do_pack(c)
    if not archive_path:
        return False
    
    return do_deploy(c, archive_path)
