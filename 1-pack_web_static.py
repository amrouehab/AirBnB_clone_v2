#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of web_static
"""
from fabric import task
from datetime import datetime
import os


@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of web_static folder
    
    Returns:
        str: path to archive if successful, None otherwise
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")
        
        # Generate archive path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        
        # Create tar archive
        c.local("tar -cvzf {} web_static".format(archive_path))
        
        return archive_path
    except Exception:
        return None
