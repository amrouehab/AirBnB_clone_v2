#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric import task
import os

env.hosts = ['<IP web-01>', 'IP web-02']


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
        # Upload archive to /tmp/ directory
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace('.tgz', '')
        remote_path = '/tmp/{}'.format(file_name)
        release_path = '/data/web_static/releases/{}'.format(folder_name)
        
        # Upload the archive
        c.put(archive_path, remote_path)
        
        # Create release directory
        c.run('mkdir -p {}'.format(release_path))
        
        # Extract archive
        c.run('tar -xzf {} -C {}'.format(remote_path, release_path))
        
        # Remove archive
        c.run('rm {}'.format(remote_path))
        
        # Move contents to proper location
        c.run('mv {}/web_static/* {}/'.format(release_path, release_path))
        c.run('rm -rf {}/web_static'.format(release_path))
        
        # Remove old current link and create new one
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {} /data/web_static/current'.format(release_path))
        
        print('New version deployed!')
        return True
    except Exception:
        return False
