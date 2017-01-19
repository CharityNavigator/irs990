# IRS 990 Toolkit (UNDER DEVELOPMENT)

This repository contains everything you need to get started exploring the IRS 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/). This includes instructions for an easier-to-use 990 database provided free to the public by [Charity Navigator](https://www.charitynavigator.org/).

## Why we are providing these files

Charity Navigator is dedicated to the advancement of informed and intelligent giving. The IRS 990 is a crucial public record of nonprofit governance, but the original electronic records are very hard to work with.

The original 990 dataset consists of more than a million individual files. The encoding scheme for these files varies from case to case, and the file structure alone makes them very difficult to retrieve. The tools offered here are intended to facilitate retrieval, comprehension and analysis.

This toolkit is neither perfect nor comprehensive, but we hope it can be a starting point for data scientists and subject area experts looking to explore public records for the charitable sector.

## What is available here:

This toolkit encompasses several offerings, along with documentation about how to use each one.

* **A small database capturing selected fields from the IRS 990 from tax years 2011 to 2014.** The fields chosen are those most helpful to Charity Navigator. You may find them helpful as well. [Click for more info.](http://placeholder.com)

* **A large database capturing the above fields, plus all of the raw 990 data in an indexed and searchable form.** The 990 data provided by the IRS can be slow to search,  download and retrieve. This database is designed to provide the raw data in a more easily searchable form. By associating the raw data with pre-digested fields, it is possible to do selective data pulls on specific criteria.  [Click for more info.](http://placeholder.com)

* **(ADVANCED USERS ONLY) Code and instructions for rebuilding the above databases.** All of the code used to build this database is available in this repository. If you wish to add additional fields to the database provided here, or if you wish to build our logic into your application, use this logic. Note that this is expensive and depends on Apache Spark. You should do it only if you know what you're doing!  [Click for more info.](http://placeholder.com)

* **Preliminary views into the data.** We have provided several visualizations of the data, along with the R code used to generate it.  [Click for more info.](http://placeholder.com)

## Who should use this toolkit

These tools were prepared for researchers, data scientists, and enthusiasts interested in exploring the IRS 990 database. These tools are partial and preliminary, but they can help get you over the hump if you've been stuck on this difficult-to-use dataset. You should **not** use this dataset for legal investigations, policy decisions, or published findings without some scrutiny and careful cleaning. If you do polish things up, please consider contributing to this repository.

## Prerequisites

These tools assume that you are comfortable working with SQL databases, and have at least a passing familiarity with Amazon Web Services and the Linux command line. Also, you must be willing to spend a modest amount of money to set up a copy of the smallest database, plus hourly hosting fees; expect to spend more on the large database or to build from scratch. The software we are providing is free; Amazon Web Services is not.

## Limitations

The following limitations apply as of the latest version we are hosting.

* **990 data only.** The AWS dataset contains both 990 and 990-EZ filings. As of this version, the toolkit only provides support for 990 filings. 
* **No 2015 data.** The AWS dataset contains data from 2011 through 2015. As of this version, the toolkit only provides support for filings through 2015.
* **As with all complex datasets, there will be flaws, mistakes, and bugs in our database.** Some of these are already known. See the [issues page](https://github.com/CharityNavigator/irs990/issues) for known bugs. If you find something wrong, please [report an issue](https://github.com/CharityNavigator/irs990/issues).

## Getting started

### Building a database

 * The easiest, cheapest way to get started is to clone a copy of the IRS database from our S3 mirror. [Instructions](https://github.com/CharityNavigator/irs990/blob/master/documentation/clone_database.md)
 * If our files are out of date, or if you wish to customize your database, please follow our tutorial for building the database from scratch. [Instructions](http://placeholder/)

### Exploring the schema

If you're just getting started with the AWS 990 dataset, you may wish to explore the structure of the data. We are building a tool for visualizing and exploring the dataset at a high level. The tool is currently being built from the ground up. If you are interested in a preview of the visualization tool, please [contact us](mailto:dborenstein@charitynavigator.org).

## Authors

Code, documentation, and visualizations: David Bruce Borenstein
Crosswalk between XML and database columns: Vince Bogucki

## Notice

*Copyright (c) 2017 Charity Navigator.*

*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*
