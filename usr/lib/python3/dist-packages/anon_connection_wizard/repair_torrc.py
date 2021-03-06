#!/usr/bin/python3 -u

## Copyright (C) 2018 - 2020 ENCRYPTED SUPPORT LP <adrelanos@riseup.net>
## See the file COPYING for copying conditions.

import fileinput, os, shutil
from subprocess import check_output, STDOUT, call, Popen, PIPE

if os.path.exists('/usr/share/anon-gw-base-files/gateway'):
    whonix=True
else:
    whonix=False

def repair_torrc():
   if not whonix:
      ## Not implemented for non-Whonix yet.
      return

   try:
      command = ['/usr/lib/anon-gw-anonymizer-config/tor-config-sane']
      p = Popen(command, stdout=PIPE, stderr=PIPE)
      stdout, stderr = p.communicate()
   except:
      error_msg = "tor-config-sane unexpected error: " + str(sys.exc_info()[0])
      print(error_msg)
