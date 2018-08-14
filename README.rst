===============================
EasyHCP
===============================

.. image:: https://img.shields.io/travis/shreyaspadhy/easyhcp.svg
        :target: https://travis-ci.org/shreyaspadhy/easyhcp

.. image:: https://img.shields.io/pypi/v/easyhcp.svg
        :target: https://pypi.python.org/pypi/easyhcp


Python Package for Easy Scraping and Handling of HCP Data

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://shreyaspadhy.github.io/easyhcp.

Quick Tutorial
--------------
1. To quickly get started, and seet up AWS credentials (if you already haven't), run the following - 
```
import easyhcp
hcpscraper.setup_credentials()
```
2. To get preprocessed, registered structural data for a list of subjects, 
```
hcpscraper.get_structural_data(subject_list, scan_type, preprocessed=True, MNISpace=True, out_dir='.')
```

Features
--------
* Set up AWS Credentials to access the HCP bucket
* Get Structural Data for a list of subjects
* Get Resting-State Data for a list of subjects

Upcoming Features
-----------------
* Return a list of all/random subset of HCP subjects
* Display the directory structure and help
* Loads more data-scraping functionality
* BIDSifying scraped data
