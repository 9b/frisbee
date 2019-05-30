Changelog
=========
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