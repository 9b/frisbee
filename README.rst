Frisbee
=======
.. image:: https://readthedocs.org/projects/frisbee/badge/?version=latest
    :target: http://frisbee.readthedocs.io/en/latest/?badge=latest

.. image:: https://badge.fury.io/py/frisbee.svg
    :target: https://badge.fury.io/py/frisbee

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT


Frisbee is a small utility to collect email addresses from search engines and
other free-form text sources. Frisbee makes it simple to find email addresses
posted on the web by taking user-fed input and translating it into an
automated search query. Users can extend frisbee by adding modules for new
search engines or other obscure data sources.

Quick Start
-----------
**Install the library**:

``pip install frisbee`` or ``python setup.py install``

**Run a search**

``frisbee search -e bing -d bnpparibas.com -l 50 --greedy --save``

**Search in bulk**

``frisbee search -e bing -f domains -l 50 --save``


Sample Code
-----------

This sample code shows some of the range of functionality within the module::

    from frisbee import Frisbee

    # Create an instance
    frisbee = Frisbee(save=True)

    # Describe your job
    jobs = [{'engine': 'bing', 'modifier': 'site:github.com',
             'domain': 'foo.bar', 'limit': 50}]

    # Execute the jobs
    frisbee.search(jobs)

    # Get the results
    results = frisbee.get_results()

Example Output
--------------

Below is an example job result::

    [{
        "engine": "bing",
        "modifier": "site:github.com",
        "domain": "blockade.io",
        "limit": 50,
        "results": {
            "start_time": "2018-12-13 16:54:15",
            "end_time": "2018-12-13 16:54:19",
            "emails": [
                "info@blockade.io"
            ],
            "duration": "4",
            "processed": 44
        },
        "project": "zealous_kirch"
    }]

Features
--------
* Ability to search for email addresses from search engine results
* Modular design that can be extended easily to include new sources
* Modifier options that can filter or target search query
* Limit option to reduce the number of results parsed
* Greedy option to learn from collected results and fuzzy to find related
* Save output describing job request and results
* Individual or bulk look-ups using the command line utility

Changelog
---------
05-30-19
~~~~~~~~
* Feature: Added a bulk option to the command line tool to ease usage
* Change: Replaced multiprocessing with concurrent.futures to simplify logic
* Change: Split logic of dynamic module loading and future work outside of the Frisbee class
* Change: Reverted back to the BS4 parsing versus raw text
* Change: Replaced the regular expression processing to be more efficient
* Change: Progressively save results as they come in to avoid any losses from a deadlock
* Change: Randomize the top-level directory to avoid conflicts

05-24-19
~~~~~~~~
* Feature: Clean SERPs to remove files or other formats we can't inspect
* Change: Use text extraction instead of BS4 HTML parsing to get body of websites (ensures clean email extraction)
* Change: Increased logging and timeout parameters

12-20-18
~~~~~~~~
* Feature: Added typing to the core code
* Feature: Added a fuzzy flag to find related domains

12-14-18
~~~~~~~~
* Feature: Activated greedy option to save and output to screen
* Bugfix: Wrapped loading of HTML for cases where data is dirty

12-13-18
~~~~~~~~
* Initial push!
