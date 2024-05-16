import re
import termcolor
from sys import platform
import os
import subprocess

# Share Class

class Share:
  def __init__(self, name, path, uname, passwd):
    self.name = name
    self.path = path
    self.uname = uname
    self.passwd = passwd



def is_sudo():
  return os.geteuid() == 0

def save_info():
  share_name = input(termcolor.colored('[!] Share name: ', 'cyan'))
  share_path = input(termcolor.colored('[!] Share path: ', 'cyan'))
  share_uname = input(termcolor.colored('[!] Share username: ', 'cyan'))
  share_passwd = input(termcolor.colored('[!] Share password: ', 'cyan'))

  name_regex = r'^[a-zA-Z0-9_-]+$'
  path_regex = r'^[a-zA-Z0-9_\-/\.]+$'
  passwd_regex = r'^[\x20-\x7E]+$'

  if not re.match(name_regex, share_name):
    print(termcolor.colored('[-] Invalid share name!', 'red'))
    return

  if not re.match(path_regex, share_path):
    print(termcolor.colored('[-] Invalid share path!', 'red'))
    return
  
  if not re.match(name_regex, share_uname):
    print(termcolor.colored('[-] Invalid share username!', 'red'))
    return
  
  if not re.match(passwd_regex, share_passwd):
    print(termcolor.colored('[-] Invalid share password!', 'red'))
    return
  
  if not os.path.exists(share_path):
    print(termcolor.colored('[-] Directory does not exist!', 'red'))
    return
  
  if not os.path.isdir(share_path):
    print(termcolor.colored('[-] Please select a directory!', 'red'))
    return
  

  share = Share(share_name, share_path, share_uname, share_passwd)
  samba_setup(share)

def samba_setup(share):
  print(termcolor.colored('[*] Setting up Samba...', 'cyan'))
  os.system(f'sudo echo [{share.name}] >> /etc/samba/smb.conf')
  print(termcolor.colored('[!] Setting up permissions...', 'cyan'))

  read_only = input(termcolor.colored('[!] Read only? (y/n): ', 'cyan'))
  if read_only == 'y':
    os.system(f'sudo echo read only = yes >> /etc/samba/smb.conf')
  else:
    os.system(f'sudo echo read only = no >> /etc/samba/smb.conf')

  browsable = input(termcolor.colored('[!] Browsable? (y/n): ', 'cyan'))
  if browsable == 'y':
    os.system(f'sudo echo browsable = yes >> /etc/samba/smb.conf')
  else:
    os.system(f'sudo echo browsable = no >> /etc/samba/smb.conf')

  available = input(termcolor.colored('[!] Available? (y/n): ', 'cyan'))
  if available == 'y':
    os.system(f'sudo echo available = yes >> /etc/samba/smb.conf')
  else:
    os.system(f'sudo echo available = no >> /etc/samba/smb.conf')

  guest_ok = input(termcolor.colored('[!] Guest ok? (y/n): ', 'cyan'))
  if guest_ok == 'y':
    os.system(f'sudo echo guest ok = yes >> /etc/samba/smb.conf')
  else:
    os.system(f'sudo echo guest ok = no >> /etc/samba/smb.conf')

  writable = input(termcolor.colored('[!] Writable? (y/n): ', 'cyan'))
  if writable == 'y':
    os.system(f'sudo echo writable = yes >> /etc/samba/smb.conf')
  else:
    os.system(f'sudo echo writable = no >> /etc/samba/smb.conf')

  os.system(f'sudo echo valid users = {share.uname} >> /etc/samba/smb.conf')
  os.system(f'sudo echo comment = {share.name} >> /etc/samba/smb.conf')

  os.system(f'sudo echo path = {share.path} >> /etc/samba/smb.conf')

  os.system(f'(echo {share.passwd}; echo {share.passwd}) | sudo smbpasswd -a {share.uname}')

  os.system('sudo systemctl start smbd.service')
  os.system('sudo systemctl restart smbd.service')


if not is_sudo():
  print(termcolor.colored('[-] No sudo privilege! Stopping...', 'red'))
  exit()

if platform == "linux" or platform == "linux2":
  print(termcolor.colored('[*] Linux detected', 'green'))
  path = '/etc/samba/smb.conf'
  if os.path.isfile(path):
    print(termcolor.colored('[*] Samba found!', 'green'))
  else:
    print(termcolor.colored('[-] Samba NOT found!', 'red'))

  save_info()

else:
  print(termcolor.colored('[-] Unsupported platform!', 'red'))
  exit()
