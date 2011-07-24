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
    searching through the use of the `date:` search-term. See "Current
    Enhancements" section below.


 3. ...and note, this is *not* implemented yet, but... To move
    decryption and verification to client side during remote usage in
    order to avoid having a key on numerous computers, and to remove
    the need for any X-tunneled pinentry programs.

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

The current configuration options are supported:

  * `general` settings

      + `account`: which account (set below) to use. If none set, this
        will default to local usage with default `notmuch` binary and
        configuration file.

      + `ssh_bin`: which ssh binary to use. Defaults to `ssh`.

  * `${account}`settings. (Note: you can have numerous accounts, and
    the one used will be determined by the `notmuch` setting in `general`.

      + `remote`: yes/[no]

      + `server`: server to user if `remote` is yes. (Setting remote
        to "yes" and not setting a server will be an error.)

      + `user`: user for server. Defaults to current logged-in user.

      + `private_key` private-key for key-pair
        authentication. Defaults to openssh's setting. [Not yet
        implemented]

      + `notmuch_config`: The configuration file to use for notmuch
        (either on the local or remote computer, depending on the
        value set for `remote`). Defaults to notmuch's default.

      + `notmuch_bin`: The notmuch binary to use (either on the local
        or remote computer, depending on the value set for
        `remote`). Defaults to `notmuch`, leaving the rest up to your
        ${PATH} environment.

      + `cache`: The cache to use for remote usage. Defaults to
        `~/.notmuch-client-cache.d`. **IMPORTANT NOTE:** At the
        moment, using the same cache for different remote accounts
        *will* have unexpected results. Make sure to set different
        caches if you have more than one remote account. This will be
        enforced in the future.

Usage
-----

Just add the installation folder to your path, and run
`notmuch-client`, or -- what I do -- make `notmuch` a link to
`notmuch-client`.

A future version will add distutils setup.

Current Enhancements
--------------------

  * search:

      + You can search for **date ranges** using the search prefix
        `date:` and the syntax:
            
            date:YYYY-M-D--YYYY-M-D

        Note that years and months are optional, though to avoid
        ambiguity, you must enter a month if you enter a year. If year
        or month is not specified in the beginning of the range, it
        will default to the current year or month. If it is not
        specified in the end of the range, it will default to the year
        or month in the beginning of the range.

        If either the first or last date is left off altogether, it
        will default to a range between the beginning and end of time
        (i.e. 1 Jan 1970 and today). (Today is not really the end of
        time, don't worry.)

        So, assuming that it's currently 23 July, 2011:

           date:3-11--4-25

        will mean the range between 2011-3-11 and 2011-4-25.

           date:2009-3-11--4-25

        will mean the range between 2009-3-11 and 2009-4-25.

           date 2009-3-11--

        will mean the range between 2009-3-11 and today.







