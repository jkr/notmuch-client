notmuch-client
==============

A client wrapper for notmuch. 

The aims of notmuch-client
--------------------------

 1. To make remote usage on notmuch as transparent as
    possible. 

    notmuch-client currently allows you to connect to a notmuch
    installation over ssh, and caches message bodies locally to avoid
    unnecessary downloading. It also allows for local usage, and for
    easy switching, through a configuration file, between different
    databases or configurations

 2. To allow users to supplement certain commands without needing to
    wade into the notmuch sources. 

    One example: notmuch-client adds more convenient date ranges to
    searching through the use of the `date:` search-term. More on this
    below.

 3. ...and note, this *not* implemented yet, but... To move decryption
    and verification to client side during remote usage in order to
    avoid having a key on numerous computers, and to remove the need
    for any X-tunneled pinentry programes.

    (This part won't be *too* hard, but it will require replicating
    notmuch's undocumented JSON format, which might be something of a
    moving target.)

Installation and Configuration
------------------------------

Currently the best way to install is just to cd into the nmclient
folder, and run the notmuch-client executable from there. Soon I will
add a distutils setup script.

notmuch-client looks for its configuration in
`~/.notmuch-client.config`. An example configuration file can be found
in `examples/notmuch-client.config`.






