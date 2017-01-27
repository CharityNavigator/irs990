# IRS 990 Toolkit (UNDER DEVELOPMENT)

This repository contains everything you need to get started exploring the IRS 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/). This includes instructions for an easier-to-use 990 database provided free to the public by [Charity Navigator](https://www.charitynavigator.org/).

## Why we are providing these files

Charity Navigator is dedicated to the advancement of informed giving. The IRS 990 is a crucial public record of nonprofit governance, but the original electronic records are very hard to work with.

The original 990 dataset consists of more than a million individual files. The encoding scheme for these files varies from case to case, and the file structure alone makes them very difficult to retrieve. The tools offered here are intended to facilitate retrieval, comprehension and analysis.

This toolkit is neither perfect nor comprehensive, but we hope it can be a starting point for data scientists and subject area experts looking to explore public records for the charitable sector.

## What is available here:

We recommend using our [quick start](https://charitynavigator.github.io/irs990/quick-start), but we provide other options as well.

* **[Quick-start option](https://charitynavigator.github.io/irs990/quick-start) (recommended):** Create a virtual machine on Amazon EC2 with the database and RStudio pre-installed, along with a quick-start tutorial to begin exploring quickly. [[Click for more info.]](https://charitynavigator.github.io/irs990/quick-start)

* **[Clone our database](https://charitynavigator.github.io/irs990/clone-database):** Download a snapshot of the 990 database as a `.sql` file, and load it into a MySQL (or similar) database. [[Click for more info.]](https://charitynavigator.github.io/irs990/clone-database)

* **[Build from scratch](https://charitynavigator.github.io/irs990/create-database):** For advanced users who wish to modify or extend the 990 toolkit, we provide instructions for building the database from scratch. [[Click for more info.]](https://charitynavigator.github.io/irs990/create-database)

## Who should use this toolkit

These tools were prepared for researchers, data scientists, and enthusiasts interested in exploring the IRS 990 database. These tools are partial and preliminary, but they can help get you get started working with some have found to be a difficult-to-use dataset. You should **not** use this dataset for legal investigations, policy decisions, or published findings without some scrutiny and careful cleaning. If you do polish things up, please consider contributing to this repository.

## Prerequisites

The quick start assumes that you are comfortable with R and RStudio, and have at least a passing familiarity with relational databases and Amazon Web Services. The other options require more expertise.

## Limitations

The following limitations apply as of the latest version we are hosting.

* **Data quality issues -- our own and upstream.** This project is new and under development. It is also based on a messy, evolving, human-created dataset whose schema varies from year to year. We are aware of several [issues](https://github.com/CharityNavigator/irs990/issues) regarding our own work. There are also numerous upstream issues upstream issues coming from the IRS or the filers themselves. We discuss some of these issues in our [documentation](https://github.com/CharityNavigator/irs990/blob/master/docs/explore-database.md).
* **990 data only.** The AWS dataset contains both 990 and 990-EZ filings. As of this version, the toolkit only provides support for 990 filings. 
* **No 2015 data.** The AWS dataset contains data from 2011 through 2015. As of this version, the toolkit only provides support for filings through 2015.
* **As with all complex datasets, there will be flaws, mistakes, and bugs in our database.** Some of these are already known. See the [issues page](https://github.com/CharityNavigator/irs990/issues) for known bugs. If you find something wrong, please [report an issue](https://github.com/CharityNavigator/irs990/issues).

## Getting started

### Building a database

 * The easiest, cheapest way to get started is to clone a copy of the IRS database from our S3 mirror. [[Instructions]](https://github.com/CharityNavigator/irs990/blob/master/documentation/clone_database.md)
 * If our files are out of date, or if you wish to customize your database, please follow our tutorial for building the database from scratch. [[Instructions]](https://github.com/CharityNavigator/irs990/blob/master/docs/create-database.md)

### Exploring the schema

If you're just getting started with the AWS 990 dataset, you may wish to explore the structure of the data. We are building a tool for visualizing and exploring the dataset at a high level. The tool is currently being built from the ground up. If you are interested in a preview of the visualization tool, please [contact us](mailto:dborenstein@charitynavigator.org).

### Change log

After the initial release, check here for updates about changes to the database.

## Authors

Code and visualizations: David Bruce Borenstein

Documentation: David Bruce Borenstein and Zach Weinsteiger

Crosswalk between XML and database columns (990): Vince Bogucki

Crosswalk between XML and database columns (EZ): David Bruce Borenstein and Zach Weinsteiger
