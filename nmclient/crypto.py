# -*-  coding: utf-8  -*-
#########################################################################
# crypto.py: functions for use with encryption and verification         #
#                                                                       #
# Copyright © 2011 Jesse Rosenthal                                      #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see http://www.gnu.org/licenses/ .  #
#                                                                       #
# Author: Jesse Rosenthal <jrosenthal@jhu.edu>                          #
#########################################################################

from nmclient.bundled.gnupg import gnupg
import tempfile
import os
from cStringIO import StringIO

class NotmuchClientCryptoError(Exception):
    pass

def verify(multipart_signed_msg):
    parts = multipart_signed_msg.get_payload()
    data_part = parts[0]
    sig_part = parts[1]

    # Note -- we're doing as_string here, because get_payload can
    # mangle newlines.
    data = data_part.as_string()
    sig = sig_part.get_payload()
    sig_fp = StringIO(sig)

    gpg = gnupg.GPG()
    (fd, data_file) = tempfile.mkstemp()
    os.write(fd, data)
    os.close(fd)
    verification = gpg.verify_file(sig_fp, data_file)
    os.remove(data_file)

    return verification

def decrypt(multipart_encrypted_msg):
    parts = multipart_encrypted_msg.get_payload()
    encrypted_part = parts[1].get_payload()

    gpg = gnupg.GPG()
    decryption = gpg.decrypt(encrypted_part)

    return (decryption.valid, decryption.data)




    



