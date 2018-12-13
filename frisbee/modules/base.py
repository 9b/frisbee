#!/usr/bin/env python
import logging
import requests
from requests_futures.sessions import FuturesSession
from concurrent.futures import wait
from frisbee.utils import gen_logger
from frisbee.utils import gen_headers


class Base(object):

    """Base module class to assist in writing new modules."""

    name = 'base'
    log = gen_logger(name, logging.INFO)
    limit = 500

    def __init__(self, log_level=logging.INFO):
        """Local variables for the module."""
        self.set_log_level(log_level)

    def set_log_level(self, level):
        """Override the default log level of the class."""
        if level == 'info':
            level = logging.INFO
        if level == 'debug':
            level = logging.DEBUG
        if level == 'error':
            level = logging.ERROR
        self.log.setLevel(level)

    def _request_bulk(self, urls):
        """Batch the requests going out."""
        if len(urls) == 0:
            raise Exception("No results were found")
        session = FuturesSession(max_workers=len(urls))
        self.log.info("Bulk requesting: %d" % len(urls))
        futures = [session.get(u, headers=gen_headers(), timeout=3) for u in urls]
        done, incomplete = wait(futures)
        results = list()
        for response in done:
            try:
                results.append(response.result())
            except Exception as err:
                self.log.warn("Failed result: %s" % err)
        return results

    def search(self):
        """Execute search function and hand to processor."""
        raise NotImplementedError

    def _format(self):
        """Format search queries to perform in bulk.

        Build up the URLs to call for the search engine. These will be ran
        through a bulk processor and returned to a detailer.
        """
        raise NotImplementedError

    def _process(self, responses):
        """Process search engine results for detailed analysis.

        Search engine result pages (SERPs) come back with each request and will
        need to be extracted in order to crawl the actual hits.
        """
        raise NotImplementedError

    def _fetch(self, urls):
        """Perform bulk collection of data and return the content.

        Gathering responses is handled by the base class and uses futures to
        speed up the processing. Response data is saved inside a local variable
        to be used later in extraction.
        """
        raise NotImplementedError

    def _extract(self):
        """Extract email addresses from results.

        Text content from all crawled pages are ran through a simple email
        extractor. Data is cleaned prior to running pattern expressions.
        """
        raise NotImplementedError
