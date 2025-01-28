#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
"""
from fabric import task
import os

env.hosts = ['<IP web-01>', 'IP web-02']


@task
def do_clean(c, number=0):
    """
    Deletes out-of-date archives
    
    Args:
        number (int): Number of archives to keep (including most recent)
        
    If number is 0 or 1, keeps only the most recent version
    If number is 2, keeps the most and second most recent versions
    """
    # Convert number to integer and ensure it's at least 0
    try:
        n = int(number)
    except:
        return False
    if n < 0:
        return False
        
    # If number is 0 or 1, we only keep one archive
    if n == 0:
        n = 1
        
    try:
        # Clean local archives in versions folder
        if os.path.exists("versions"):
            archives = sorted(os.listdir("versions"))
            archives = [a for a in archives if a.endswith(".tgz")]
            [os.remove("versions/{}".format(a)) for a in archives[:-n]]
            
        # Clean remote archives on both web servers
        with c.cd('/data/web_static/releases'):
            archives = c.run('ls -t').stdout.split()
            archives = [a for a in archives if a.startswith('web_static_')]
            [c.run('rm -rf {}'.format(a)) for a in archives[n:]]
            
        return True
    except Exception:
        return False
