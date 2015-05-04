#!/usr/bin/env python
"""
nitwit

Searches Twitter for usernames from word list. Reads words from 
/usr/share/dict/words by default. Requires the requests library.

Licensed under the MIT License.

Copyright (c) 2015 Abhi Nellore.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

DISCLAIMER: The author (Abhi Nellore) is not responsible for other users'
misuse or abuse of this script.
"""
try:
    import requests
except ImportError:
    raise ImportError('nitwit requires the requests library. Install it by '
                      'running "pip install requests".')
import os.path
import sys
import time
import urllib

_error_429 = ('Twitter\'s spouting 429s; too many requests are being made of '
              'the server. Wait a while, or download Tor '
              '(https://www.torproject.org/), set up a SOCKS5 proxy, and '
              'specify its port at the command line with "-p".')

def available(username, proxies={}, is_404=False):
    """ Checks if Twitter username is available.

        username: string with username
        proxies: keyword argument "proxies" of requests.get()
        is_404: queries for username directly to check for 404; a 404 is
            a necessary but not sufficient condition for username availability

        Return value: True if username is available; else False.
    """
    if is_404:
        request = requests.get(
                    'http://twitter.com/' + urllib.quote_plus(username),
                    proxies=proxies
                )
        if request.status_code == 429:
            raise RuntimeError(_error_429)
        return (request.status_code == 404)
    else:
        request = requests.get(
                    'http://twitter.com/users/username_available?username='
                    + urllib.quote_plus(username),
                    proxies=proxies
                )
    try:
        to_return = request.json()['valid']
    except ValueError:
        if request.status_code == 429:
            raise RuntimeError(_error_429)
        raise
    return to_return

def write_available_usernames(words, suppress_status=False, proxy=None,
                                wait=0.25, maybe=-1):
    """ Writes word if it is an available Twitter username.

        words: iterable of words
        suppress_status: True if stats on search should not be printed to
            stderr
        proxies: None if no proxy is to be used; else https proxy IP
        wait: how long to wait (in s) between successive requests
        maybe: -1 if a username should be annotated with "<tab>m" if it
            has no associated account but is reported as unavailable; 0 if
            all usernames with no associated accounts should be written;
            1 if only usernames explicitly reported as available should be
            written

        No return value.
    """
    if proxy is None:
        proxies = {}
    else:
        proxies = { 'http' : proxy, 'https' : proxy }
    if suppress_status:
        status_stream = open(os.devnull, 'w')
    else:
        status_stream = sys.stderr
    found = 0
    min_word_length = None
    error_string = ('\x1b[Kmin word length found: {min_word_length} || '
                    'words found: {found} || last word searched: {word}\r')
    for k, word in enumerate(words):
        to_write = None
        if maybe == -1:
            if available(word, proxies=proxies, is_404=True):
                to_write = [word]
                if not available(word, proxies=proxies):
                    to_write.append('m')
        elif maybe == 0:
            if available(word, proxies=proxies, is_404=True):
                to_write = [word]
        elif maybe == 1:
            if available(word, proxies=proxies):
                to_write = [word]
        if to_write is not None:
            print '\t'.join(to_write)
            sys.stdout.flush()
            word_length = len(word)
            try:
                if min_word_length - word_length > 0:
                    min_word_length = word_length
            except TypeError:
                min_word_length = word_length
            found += 1
        print >>status_stream, error_string.format(
                min_word_length=min_word_length,
                found=found,
                word=word
            ),
    time.sleep(wait)

if __name__ == '__main__':
    import argparse
    # Print file's docstring if -h is invoked
    parser = argparse.ArgumentParser(description=__doc__, 
                formatter_class=argparse.RawDescriptionHelpFormatter)
    # Add command-line arguments
    parser.add_argument('--suppress-status', '-s', action='store_const',
            const=True,
            default=False,
            help='suppresses status updates written to stderr'
        )
    parser.add_argument('--dictionary', '-d', type=str,
            default='/usr/share/dict/words',
            help=('text file with a different word on each line. use "-" to '
                  'read from stdin')
        )
    parser.add_argument('--proxy', '-p', type=str,
            default=None,
            help=('proxy including port (ex: http://10.10.1.10:1080); useful '
                  'in conjunction with Tor if 429s are encountered, but '
                  'do not abuse')
        )
    parser.add_argument('--wait', '-w', type=float,
            default=0.25,
            help='how long to wait (in s) between successive requests'
        )
    parser.add_argument('--maybe', '-m', type=str,
            default='annotate',
            help=('choose from among {"yes", "no", "annotate"). a username '
                  'with no associated account may be reported as unavailable.'
                  'if "yes", include it in output (1 request/word). if '
                  '"no", do not include it in output (1 request/word). if '
                  '"annotate", write "<tab>m" after each of them '
                  '(2 requests/word).')
        )
    args = parser.parse_args()
    if args.wait < 0:
        raise ValueError('Wait time ("--wait", "-w") must take a value > 0, '
                         'but {} was entered.'.format(args.wait))
    if args.dictionary == '-':
        if sys.stdin.isatty():
            raise RuntimeError('stdin was specified as the dictionary, but no '
                               'data was found there. Specify a dictionary '
                               'file with "-d <file>", or pipe a command into '
                               'this script.')
        write_available_usernames((line.strip().split('\t')[0] for line
                                        in sys.stdin),
                                    suppress_status=args.suppress_status,
                                    proxy=args.proxy)
    if args.maybe not in ['annotate', 'yes', 'no']:
        raise RuntimeError('Maybe argument ("--maybe", "-m") must be one '
                           'of {"annotate", "yes", "no"}, '
                           'but {} was entered'.format(args.maybe))
    elif not os.path.isfile(args.dictionary):
        raise RuntimeError(
                '"{}" is not a valid dictionary file. Try again.'.format(
                        args.dictionary
                    )
            )
    else:
        with open(args.dictionary) as dictionary_stream:
            write_available_usernames((line.strip().split('\t')[0] for line
                                        in dictionary_stream),
                                        suppress_status=args.suppress_status,
                                        proxy=args.proxy,
                                        wait=args.wait,
                                        maybe=(-1 if args.maybe == 'annotate'
                                                else (0 if args.maybe == 'yes'
                                                    else 1)
                                                    )
                                                )