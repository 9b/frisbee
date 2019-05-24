#!/usr/bin/env python
import datetime
import logging
import os
import random
import re
import sys
from typing import Dict
from typing import List
from typing import Pattern


EXTENSIONS = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'png', 'jpg', 'tiff', 'gif',
              'jpeg', 'psd', 'eps', 'raw', 'zip', 'exe', 'dmg', 'tar', 'tgz',
              'iso', 'rar', 'rpm', 'bin', 'jar', 'xls', 'xlsx']


def gen_logger(name: str, log_level: int=logging.INFO) -> logging.Logger:
    """Create a logger to be used between processes.

    :returns: Logging instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    shandler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    fmt: str = '\033[1;32m%(levelname)-5s %(module)s:%(funcName)s():'
    fmt += '%(lineno)d %(asctime)s\033[0m| %(message)s'
    shandler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(shandler)
    return logger


def gen_headers() -> Dict[str, str]:
    """Generate a header pairing."""
    ua_list: List[str] = ['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36']
    headers: Dict[str, str] = {'User-Agent': ua_list[random.randint(0, len(ua_list) - 1)]}
    return headers


def str_datetime(stamp: datetime.datetime) -> str:
    """Convert datetime to str format."""
    return stamp.strftime("%Y-%m-%d %H:%M:%S")


def now_time() -> datetime.datetime:
    """Get the current time."""
    return datetime.datetime.now()


def extract_emails(results: str, domain: str, fuzzy: bool) -> List[str]:
    """Grab email addresses from raw text data."""
    pattern: Pattern = re.compile(r'([\w.-]+@[\w.-]+)', re.IGNORECASE)
    hits: List[str] = list(set(pattern.findall(results)))
    if fuzzy:
        seed = domain.split('.')[0]
        emails: List[str] = [x.lower().strip('.') for x in hits if x.split('@')[1].__contains__(seed)]
    else:
        emails: List[str] = [x.lower().strip('.') for x in hits if x.endswith(domain)]
    return list(set(emails))


def clean_urls(urls: List) -> List[str]:
    """Clean the URLs so we don't end up with large file requests."""
    tmp = list()
    for url in urls:
        url = url.lower()
        if url.split('.')[-1] in EXTENSIONS:
            continue
        tmp.append(url)
    return list(set(tmp))
