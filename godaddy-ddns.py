#!/bin/env python
import sys
import json
import argparse

if sys.version_info > (3,):
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
else:
    # noinspection PyUnresolvedReferences
    from urllib2 import urlopen, Request
    # noinspection PyUnresolvedReferences
    from urllib2 import URLError, HTTPError

program = 'godaddy-ddns'
epilog = 'GoDaddy customers can obtain values for the KEY and SECRET ' \
         'arguments by creating a production key at ' \
         'https://developer.godaddy.com/keys/. Note that command line' \
         'arguments may be specified in a FILE, one to a line, by instead' \
         'giving the argument "%FILE".  For security reasons, it is' \
         'particularly recommended to supply the KEY and SECRET arguments in ' \
         'such a file, rather than directly on the command line.'

__version__ = '0.3.0'
__author__ = 'Carl Edman (CarlEdman@gmail.com), ' \
             'Sun Ziping (sunziping2016@gmail.com)'


def get_ip(type='ipv4'):
    try:
        resp = urlopen('http://{}.icanhazip.com/'.format(type)).read()
        if sys.version_info > (3,):
            resp = resp.decode('utf-8')
        return resp.strip()
    except URLError:
        return None


def update_godaddy_record(domain, type, name, records,
                          key=None, secret=None):
    url = 'https://api.godaddy.com/v1/domains/{}/records/{}/{}'.format(
        domain, type, name)
    data = json.dumps(records)
    if sys.version_info > (3,):
        data = data.encode('utf-8')
    req = Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if key and secret:
        req.add_header("Authorization", "sso-key {}:{}".format(key, secret))
    # https://stackoverflow.com/questions/111945/is-there-any-way-to-do-http-put-in-python
    req.get_method = lambda: 'PUT'
    try:
        urlopen(req)
    except HTTPError as e:
        resp = e.read()
        if sys.version_info > (3,):
            resp = resp.decode('utf-8')
        resp = json.loads(resp)
        raise RuntimeError(resp['message'])


def main(args):
    ipv4 = get_ip('ipv4')
    ipv6 = get_ip('ipv6')
    if ipv4 is None and ipv6 is None:
        print('No ipv4 or ipv6 address available')
    if ipv4:
        update_godaddy_record(args.domain, 'A', args.name, [{
            'data': ipv4,
            'ttl': args.ttl
        }], args.key, args.secret)
        print('Successfully updated IPv4 address to {}'.format(ipv4))
    if ipv6:
        update_godaddy_record(args.domain, 'AAAA', args.name, [{
            'data': ipv6,
            'ttl': args.ttl
        }], args.key, args.secret)
        print('Successfully updated IPv6 address to {}'.format(ipv6))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update GoDaddy DNS Records.',
                                     fromfile_prefix_chars='%',epilog=epilog)

    parser.add_argument('--version', action='version',
                        version='{} {}'.format(program, __version__))

    parser.add_argument('domain', type=str,
                        help='Domain whose DNS Records are to be replaced')

    parser.add_argument('name', type=str,
                        help='DNS Record Name for which DNS Records are to be'
                             'replaced')

    parser.add_argument('--key', type=str, default='',
                        help='GoDaddy production key')

    parser.add_argument('--secret', type=str, default='',
                        help='GoDaddy production secret')

    parser.add_argument('--ttl', type=int, default=3600, help='DNS TTL')

    args = parser.parse_args()
    main(args)
