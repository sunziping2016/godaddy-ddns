# godaddy-ddns

Introduction
------------
A script for dynamically updating a GoDaddy DNS record. I use GoDaddy to host DNS for a domain and I wanted to point records in that domain to a host who's IP address changes occasionally. GoDaddy has an API to do this, so this happened.  This package, in particular this README.MD, is inspired by the equivalent for CloudFlare offered by [thatjpk](https://github.com/thatjpk/cloudflare-ddns).

The program is compatible for both Python 2 and 3.

Usage
-----
Invoke the program like this:

     usage: godaddy-ddns.py [-h] [--version] [--key KEY] [--secret SECRET]
                            [--ttl TTL]
                            domain name

    Update GoDaddy DNS Records.
    
    positional arguments:
      domain           Domain whose DNS Records are to be replaced
      name             DNS Record Name for which DNS Records are to bereplaced
    
    optional arguments:
      -h, --help       show this help message and exit
      --version        show program's version number and exit
      --key KEY        GoDaddy production key
      --secret SECRET  GoDaddy production secret
      --ttl TTL        DNS TTL.

GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at https://developer.godaddy.com/keys/.  

Note that command line arguments may be specified in a FILE, one to a line, by instead giving the argument "@FILE".  For security reasons, it is particularly recommended to supply the KEY and SECRET arguments in such a file, rather than directly on the command line:

Create a file named, e.g., `godaddy-ddns.config` with the content:

     HOSTNAME.COM
     NAME
     --key
     MY-KEY-FROM-GODADDY
     --secret
     MY-SECRET-FROM-GODADDY

Then just invoke `godaddy-ddns %godaddy-ddns.config`

Credits and Thanks
------------------
 - [thatjpk](https://github.com/thatjpk/cloudflare-ddns) for providing an example of this type of script.
 - [GoDaddy](https://www.godaddy.com/) for having an [API](https://developer.godaddy.com/).
 - [icanhazip.com](http://icanhazip.com/) for making grabbing your public IP
    from a script super easy.
 - [dhowdy](https://github.com/dhowdy) for supplying a fix to problem with updating root DNS record.
