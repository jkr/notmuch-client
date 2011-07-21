from nmclient.bundled.gnupg import gnupg
import tempfile
import os
from cStringIO import StringIO

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

    return verification.valid

def decrypt(multipart_encrypted_msg):
    parts = multipart_encrypted_msg.get_payload()
    encrypted_part = parts[1].get_payload()

    gpg = gnupg.GPG()
    decryption = gpg.decrypt(encrypted_part)

    return (decryption.valid, decryption.data)


