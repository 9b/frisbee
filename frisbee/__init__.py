#!/usr/bin/env python
import copy
import json
import logging
import os
import random
from importlib import import_module
from typing import ClassVar
from typing import Dict
from typing import List
import namesgenerator
from frisbee.utils import gen_logger
from frisbee.utils import str_datetime
from frisbee.utils import now_time
from concurrent.futures import ProcessPoolExecutor, as_completed


os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'


def dyn_loader(module: str, kwargs: str):
    """Dynamically load a specific module instance.

    The purpose of this function is to peek into the modules directory and
    load up the parsing module the user has specified. The benefit this brings
    is that we have no hardcoding for any module identification. Drop it into
    the folder and it's callable.
    """
    package_directory: str = os.path.dirname(os.path.abspath(__file__))
    modules: str = package_directory + "/modules"
    module = module + ".py"
    if module not in os.listdir(modules):
        raise Exception("Module %s is not valid" % module)
    module_name: str = module[:-3]
    import_path: str = "%s.%s" % ('frisbee.modules', module_name)
    imported = import_module(import_path)
    obj = getattr(imported, 'Module')
    return obj(**kwargs)


def collect(job):
    """Collect based on the job order.

    Ideally this would be part of the Frisbee class, but futures are not a fan
    of referencing self and prefer to have their targets outside of the class
    space.
    """
    print("Job: %s" % str(job))
    engine = dyn_loader(job['engine'], job)
    job['start_time'] = now_time()
    results = engine.search()
    job['end_time'] = now_time()
    duration: str = str((job['end_time'] - job['start_time']).seconds)
    job['duration'] = duration
    job.update({'results': results})
    return job


class Frisbee:

    """Class to interact with the core code."""

    NAME: ClassVar[str] = "Frisbee"

    def __init__(self, project: str = namesgenerator.get_random_name(),
                 log_level: int = logging.INFO, save: bool = False):
        """Creation. The moons and the planets are there."""
        self.project: str = project
        self.project += "_%d" % (random.randint(100000, 999999))
        self._log: logging.Logger = gen_logger(self.NAME, log_level)
        self.output: bool = save
        self.folder: str = os.getcwd()
        self._config_bootstrap()

        self._processed: List = list()

        self.results: List = list()
        self.saved: List = list()

    def _reset(self) -> None:
        """Reset some of the state in the class for multi-searches."""
        self.project: str = namesgenerator.get_random_name()
        self.project += "_%d" % (random.randint(100000, 999999))
        self._processed: List = list()
        self.results: List = list()

    def _config_bootstrap(self) -> None:
        """Handle the basic setup of the tool prior to user control.

        Bootstrap will load all the available modules for searching and set
        them up for use by this main class.
        """
        if self.output:
            self.folder: str = os.getcwd() + "/results"
            if not os.path.exists(self.folder):
                os.mkdir(self.folder)
            self.folder += "/" + self.project
            os.mkdir(self.folder)

    def _progressive_save(self, job) -> None:
        """Save output to a dictionary as results stream in.

        Depending on the options used, Frisbee can run for quite a long time.
        Each individual job is written after its completed and includes the
        findings along with the job details.
        """
        self._log.info("Saving results to '%s'" % self.folder)
        path: str = self.folder + "/"
        if job['domain'] in self.saved:
            return
        job['start_time'] = str_datetime(job['start_time'])
        job['end_time'] = str_datetime(job['end_time'])
        jid: int = random.randint(100000, 999999)
        filename: str = "%s_%s_%d_job.json" % (self.project, job['domain'], jid)
        handle = open(path + filename, 'w')
        handle.write(json.dumps(job, indent=4))
        handle.close()

        filename = "%s_%s_%d_emails.txt" % (self.project, job['domain'], jid)
        handle = open(path + filename, 'w')
        for email in job['results']['emails']:
            handle.write(email + "\n")
        handle.close()
        self.saved.append(job['domain'])

    def search(self, jobs: List[Dict[str, str]], executor=None) -> None:
        """Perform searches based on job orders."""
        if not isinstance(jobs, list):
            raise Exception("Jobs must be of type list.")
        self._log.info("Project: %s" % self.project)
        self._log.info("Processing jobs: %d", len(jobs))

        if not executor:
            #  Reuse the same executor pool when processing greedy jobs
            executor = ProcessPoolExecutor()

        futures = [executor.submit(collect, job) for job in jobs]
        for future in as_completed(futures):
            output = future.result()
            output.update({'project': self.project})
            self._processed.append(output['domain'])
            self.results.append(output)
            self._progressive_save(output)

            if output['greedy']:
                bonus_jobs: List = list()
                observed: List = list()
                for item in output['results']['emails']:
                    part_split = item.split('@')
                    if len(part_split) == 1:
                        continue
                    found: str = item.split('@')[1]
                    if found in self._processed or found in observed:
                        continue
                    observed.append(found)
                    base: Dict = dict()
                    base['limit'] = output['limit']
                    base['modifier'] = output['modifier']
                    base['engine'] = output['engine']
                    base['greedy'] = False
                    base['domain'] = found
                    bonus_jobs.append(base)

                if bonus_jobs:
                    self.search(bonus_jobs, executor=executor)

            self._log.info("All jobs processed")

    def get_results(self) -> List:
        """Return results from the search."""
        return self.results
