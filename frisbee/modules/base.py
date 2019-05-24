#!/usr/bin/env python
import logging
import requests
import urllib3
from requests_futures.sessions import FuturesSession
from concurrent.futures import wait
from frisbee.utils import clean_urls
from frisbee.utils import gen_logger
from frisbee.utils import gen_headers
from typing import ClassVar
from typing import Dict
from typing import List


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Base(object):

    """Base module class to assist in writing new modules."""

    name: ClassVar[str] = 'base'
    log: ClassVar[logging.Logger] = gen_logger(name, logging.DEBUG)
    limit: ClassVar[int] = 500

    def __init__(self, log_level=logging.DEBUG) -> None:
        """Local variables for the module."""
        self.set_log_level(log_level)

    def set_log_level(self, level: str) -> None:
        """Override the default log level of the class."""
        if level == 'info':
            to_set = logging.INFO
        if level == 'debug':
            to_set = logging.DEBUG
        if level == 'error':
            to_set = logging.ERROR
        self.log.setLevel(to_set)

    def _request_bulk(self, urls: List[str]) -> List:
        """Batch the requests going out."""
        if not urls:
            raise Exception("No results were found")
        urls = clean_urls(urls)
        session: FuturesSession = FuturesSession(max_workers=len(urls))
        self.log.info("Bulk requesting: %d" % len(urls))
        futures = [
            session.get(u, headers=gen_headers(), timeout=10, verify=False)
            for u in urls
        ]
        self.log.info("Requests made")
        done, _ = wait(futures)
        results: List = list()
        self.log.info("Storing results")
        for response in done:
            try:
                results.append(response.result())
            except Exception as err:
                self.log.warn("Failed result: %s" % err)
        self.log.info("Stored and returning")
        return results

    def search(self) -> None:
        """Execute search function and hand to processor."""
        raise NotImplementedError

    def _format(self) -> None:
        """Format search queries to perform in bulk.

        Build up the URLs to call for the search engine. These will be ran
        through a bulk processor and returned to a detailer.
        """
        raise NotImplementedError

    def _process(self, responses: List[str]) -> None:
        """Process search engine results for detailed analysis.

        Search engine result pages (SERPs) come back with each request and will
        need to be extracted in order to crawl the actual hits.
        """
        raise NotImplementedError

    def _fetch(self, urls: List[str]) -> None:
        """Perform bulk collection of data and return the content.

        Gathering responses is handled by the base class and uses futures to
        speed up the processing. Response data is saved inside a local variable
        to be used later in extraction.
        """
        raise NotImplementedError

    def _extract(self) -> None:
        """Extract email addresses from results.

        Text content from all crawled pages are ran through a simple email
        extractor. Data is cleaned prior to running pattern expressions.
        """
        raise NotImplementedError
