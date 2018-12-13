#!/usr/bin/env python
import copy
import json
import logging
import os
import queue
import random
from importlib import import_module
from multiprocessing import Lock, Process, Queue, current_process

import namesgenerator
from frisbee.utils import gen_logger
from frisbee.utils import str_datetime
from frisbee.utils import now_time


class Frisbee:

    """Class to interact with the core code."""

    NAME = "Frisbee"
    PROCESSES = 25
    MODULE_PATH = 'frisbee.modules'

    def __init__(self, project=namesgenerator.get_random_name(),
                 log_level=logging.INFO, save=False):
        """Creation."""
        self.project = project
        self._log = gen_logger(self.NAME, log_level)
        self.output = save
        self._config_bootstrap()

        self._unfullfilled = Queue()
        self._fulfilled = Queue()
        self._processes = list()
        self._processed = list()

        self.results = list()
        self.result_count = -1

    def _config_bootstrap(self):
        """Handle the basic setup of the tool prior to user control.

        Bootstrap will load all the available modules for searching and set
        them up for use by this main class.
        """
        if self.output:
            self.output = os.getcwd() + "/" + self.project
            os.mkdir(self.output)

    def _dyn_loader(self, module, kwargs):
        """Dynamically load a specific module instance."""
        package_directory = os.path.dirname(os.path.abspath(__file__))
        modules = package_directory + "/modules"
        module = module + ".py"
        if module not in os.listdir(modules):
            raise Exception("Module %s is not valid" % module)
        module_name = module[:-3]
        import_path = "%s.%s" % (self.MODULE_PATH, module_name)
        imported = import_module(import_path)
        obj = getattr(imported, 'Module')
        return obj(**kwargs)

    def _job_handler(self):
        """Process the work items."""
        while True:
            try:
                task = self._unfullfilled.get_nowait()
            except queue.Empty:
                break
            else:
                self._log.debug("Job: %s" % str(task))
                engine = self._dyn_loader(task['engine'], task)
                task['start_time'] = now_time()
                results = engine.search()
                task['end_time'] = now_time()
                duration = str((task['end_time'] - task['start_time']).seconds)
                task['duration'] = duration
                task.update({'results': results})
                self._fulfilled.put(task)
        return True

    def _save(self):
        """Save output to a directory."""
        self._log.info("Saving results to '%s'" % self.output)
        path = self.output + "/"
        for job in self.results:
            job['start_time'] = str_datetime(job['start_time'])
            job['end_time'] = str_datetime(job['end_time'])
            jid = random.randint(100000, 999999)
            filename = "%s_%s_%d_job.json" % (self.project, job['domain'], jid)
            handle = open(path + filename, 'w')
            handle.write(json.dumps(job, indent=4))
            handle.close()

            filename = "%s_%s_%d_emails.txt" % (self.project, job['domain'], jid)
            handle = open(path + filename, 'w')
            for email in job['results']['emails']:
                handle.write(email + "\n")
            handle.close()

    def search(self, jobs):
        """Perform searches based on job orders."""
        if not isinstance(jobs, list):
            raise Exception("Jobs must be of type list.")
        self._log.info("Project: %s" % self.project)
        self._log.info("Processing jobs: %d", len(jobs))
        for _, job in enumerate(jobs):
            self._unfullfilled.put(job)

        for _ in range(self.PROCESSES):
            proc = Process(target=self._job_handler)
            self._processes.append(proc)
            proc.start()

        for proc in self._processes:
            proc.join()

        while not self._fulfilled.empty():
            output = self._fulfilled.get()
            output.update({'project': self.project})
            self.results.append(output)

            # if output['greedy']:
            #     bonus_jobs = list()
            #     for item in output['results']['emails']:
            #         found = item.split('@')[1]
            #         if output['domain'] == found or found in self._processed:
            #             continue
            #         base = dict()
            #         base['limit'] = output['limit']
            #         base['modifier'] = output['modifier']
            #         base['engine'] = output['engine']
            #         base['greedy'] = False
            #         base['domain'] = found
            #         bonus_jobs.append(base)
            #         self._processed.append(found)
            #     self.search(bonus_jobs)

        self._log.info("All jobs processed")
        if self.output:
            self._save()

    def get_results(self):
        """Return results from the search."""
        return self.results
