#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import env, put, run
import os.path

# Define the list of host servers
env.hosts = ['54.173.103.252', '18.210.20.23']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']


def do_deploy(archive_path):
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
        # Get filename from archive path
        file_name = os.path.basename(archive_path)
        # Remove .tgz extension for folder name
        folder_name = file_name.replace('.tgz', '')
        # Define paths
        tmp_path = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}".format(folder_name)
        
        # Upload archive
        put(archive_path, '/tmp/')
        
        # Create new release directory
        run('mkdir -p {}/'.format(release_path))
        
        # Extract archive to new release directory
        run('tar -xzf {} -C {}/'.format(tmp_path, release_path))
        
        # Remove archive
        run('rm {}'.format(tmp_path))
        
        # Move contents to proper location
        run('mv {}/web_static/* {}/'.format(release_path, release_path))
        
        # Remove now-empty web_static directory
        run('rm -rf {}/web_static'.format(release_path))
        
        # Remove existing symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create new symbolic link
        run('ln -s {}/ /data/web_static/current'.format(release_path))
        
        print('New version deployed!')
        return True
        
    except Exception as e:
        print(e)
        return False
