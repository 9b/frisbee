#!/usr/bin/env python
import datetime
import logging
import os
import random
import re
import sys


def gen_logger(name, log_level=logging.INFO):
    """Create a logger to be used between processes.

    :returns: Logging instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    shandler = logging.StreamHandler(sys.stdout)
    fmt = '\033[1;32m%(levelname)-5s %(module)s:%(funcName)s():'
    fmt += '%(lineno)d %(asctime)s\033[0m| %(message)s'
    shandler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(shandler)
    return logger


def gen_headers():
    """Generate a header pairing."""
    ua_list = ['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36']
    headers = {'User-Agent': ua_list[random.randint(0, len(ua_list) - 1)]}
    return headers


def str_datetime(datetime):
    """Convert datetime to str format."""
    return datetime.strftime("%Y-%m-%d %H:%M:%S")


def now_time():
    """Get the current time."""
    return datetime.datetime.now()


def extract_emails(results, domain):
    """Grab email addresses from raw text data."""
    pattern = re.compile(r'([\w.-]+@[\w.-]+)')
    emails = pattern.findall(results)
    emails = [x.lower() for x in emails if x.endswith(domain)]
    return list(set(emails))
