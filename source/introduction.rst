Quick Start
-----------
**Install the library**:

``pip install frisbee`` or ``python setup.py install``

**Run a search**

``frisbee search -e bing -d bnpparibas.com -l 50 --save``


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