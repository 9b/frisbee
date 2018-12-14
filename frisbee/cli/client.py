#!/usr/bin/env python
"""Conduct searches for email addresses across different modules."""
import logging
import sys

from argparse import ArgumentParser
from frisbee import Frisbee


def main():
    """Run the core."""
    parser = ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    setup_parser = subs.add_parser('search')
    setup_parser.add_argument('-e', '--engine', dest='engine', required=True,
                              help='Search engine to use.',
                              choices=['bing'])
    setup_parser.add_argument('-d', '--domain', dest='domain', required=True,
                              help='Email domain to collect upon.', type=str)
    setup_parser.add_argument('-l', '--limit', dest='limit', required=False,
                              help='Limit number of results.', type=int,
                              default=100)
    setup_parser.add_argument('-m', '--modifier', dest='modifier', required=False,
                              help='Search modifier to add to the query.',
                              type=str, default=None)
    setup_parser.add_argument('-s', '--save', dest='to_save', required=False,
                              help='Save results to a file.', default=False,
                              action='store_true')
    setup_parser.add_argument('-g', '--greedy', dest='greedy', required=False,
                              help='Use found results to search more.', default=False,
                              action='store_true')
    args = parser.parse_args()

    if args.cmd == 'search':
        frisbee = Frisbee(log_level=logging.DEBUG, save=args.to_save)
        jobs = [{'engine': args.engine, 'modifier': args.modifier,
                 'domain': args.domain, 'limit': args.limit,
                 'greedy': args.greedy}]
        frisbee.search(jobs)
        results = frisbee.get_results()
        for job in results:
            print("-= %s Details =-" % job['project'].upper())
            print("\t[*] Engine: %s" % job['engine'])
            print("\t[*] Domain: %s" % job['domain'])
            print("\t[*] Modifer: %s" % job['modifier'])
            print("\t[*] Limit: %d" % job['limit'])
            print("\t[*] Duration: %s seconds" % job['duration'])

            print("\n-= Email Results=-")
            for email in job['results']['emails']:
                print(email)
            print("")

    sys.exit(1)
