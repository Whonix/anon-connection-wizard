#!/usr/bin/python3 -u

import sys, fileinput
import os, time
from subprocess import call
from anon_connection_wizard import repair_torrc

anon_connection_wizard_torrc_path = '/usr/local/etc/torrc.d/40_anon_connection_wizard.torrc'

def tor_status():
    if not os.path.exists(anon_connection_wizard_torrc_path):
        return 'no_torrc'

    fh = open(anon_connection_wizard_torrc_path,'r')
    lines = fh.readlines()
    fh.close()

    line_exists = False
    for line in lines:
        if line.strip() == '#DisableNetwork 0':
            line_exists = True
            return 'tor_disabled'
        elif line.strip() == 'DisableNetwork 0':
            line_exists = True
            return 'tor_enabled'

    if not line_exists:
        return 'bad_torrc'

'''Unlike tor_status() function which only shows the current state of the anon_connection_wizard.torrc,
set_enabled() and set_disabled() function will try to repair the missing torrc or
DisableNetwork line by calling repair_torrc module.
This makes sense because when we call set_enabled() or set_disabled() we really want Tor to work,
rather than receive a 'no_torrc' or 'bad_torrc' complain, which is not helpful for users.
'''
def set_enabled():
    command = 'systemctl --no-pager restart tor@default'
    tor_status = call(command, shell=True)

    if tor_status != 0:
        return 'cannot_connect'
    
    command = 'systemctl --no-pager status tor@default'
    tor_status = call(command, shell=True)
    
    if tor_status != 0:
        return 'cannot_connect'
    
    return 'tor_already_enabled'

def set_disabled():
    command = 'systemctl --no-pager stop tor@default'
    call(command, shell=True)

    return 'tor_disabled'
