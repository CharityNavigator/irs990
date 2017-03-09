# IRS Form 990 Decoder

This repository contains everything you need to get started exploring the IRS Form 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/). This includes instructions for an easier-to-use 990 database provided free to the public by [Charity Navigator](https://www.charitynavigator.org/).

## Why we are providing these files

Charity Navigator is dedicated to the advancement of informed giving. In the United States, most organizations exempt from income tax under section 501(a) must file an annual information return called the Form 990. These documents contain a wealth of information about each organization’s operations, finances and governance practices. Philanthropists, regulators, researchers and others rely on the  IRS Form 990 as a crucial public record of nonprofit governance. 

Historically, these documents were completed and mailed into the IRS. More recently, organizations began to submit them digitally. And within the last year, the IRS began to make the digitized data available to the public. 

While this is a great advancement for the sector, many have found these  original electronic records to be difficult to work with. That’s because the original Form 990 dataset consists of more than a million individual files. The encoding scheme for these files varies from case to case, and the file structure alone makes them very difficult to retrieve. The tools offered here are intended to facilitate retrieval, comprehension and analysis.

This toolkit is neither perfect nor comprehensive, but we hope it can be a starting point for data scientists and subject area experts looking to explore public records for the charitable sector.

## Getting started

We recommend using our [quick start](https://charitynavigator.github.io/irs990/quick-start), but we provide other options as well.

* **[Quick-start option](https://charitynavigator.github.io/irs990/quick-start) (recommended):** Create a virtual machine on Amazon EC2 with the database and RStudio pre-installed, along with a quick-start tutorial to begin exploring quickly. [[Click for more info.]](https://charitynavigator.github.io/irs990/quick-start)

* **[Clone our database](https://charitynavigator.github.io/irs990/clone-database):** Download a snapshot of the Form 990 Decoder database as a `.sql` file, and load it into a MySQL (or similar) database. [[Click for more info.]](https://charitynavigator.github.io/irs990/clone-database)

* **[Build from scratch](https://charitynavigator.github.io/irs990/create-database):** For advanced users who wish to modify or extend the Form 990 Decoder, we provide instructions for building the database from scratch. [[Click for more info.]](https://charitynavigator.github.io/irs990/create-database)

## Additional documentation

In addition to the documentation for each start-up option above, we also provide the following documentation:

* **[Data dictionary](http://990.charitynavigator.org/explore-database):** A description of each field and table included in our database.

* **[Github index](https://github.com/CharityNavigator/irs990):** A description of how the project is built, including a description of the files involved.

* **[Version history](http://990.charitynavigator.org/versions):** A list of release versions, with download links and descriptions of changes.

* **[Frequently asked questions](http://990.charitynavigator.org/faq)** 

* **[R tutorial](http://990.charitynavigator.org/tutorial.R)** The tutorial that appears when you follow the quick-start instructions for our **small** database.


## Who should use this toolkit

These tools were prepared for researchers, data scientists, and enthusiasts interested in exploring the IRS 990 database. These tools are partial and preliminary, but they can help you get started working with what some have found to be a difficult-to-use dataset. You should **not** use this dataset for legal investigations, policy decisions, or published findings without some scrutiny and careful cleaning. If you do polish things up, please consider contributing to this repository.

## Prerequisites

The quick start assumes that you are comfortable with R and RStudio, and have at least a passing familiarity with relational databases and Amazon Web Services. The other options require more expertise.

## Limitations

The following limitations apply as of the latest version we are hosting.

* **Data quality issues -- our own and upstream.** This project is new and under development. It is also based on a messy, evolving, human-created dataset whose schema varies from year to year. We are aware of several [issues](https://github.com/CharityNavigator/irs990/issues) regarding our own work. There are also numerous upstream issues coming from the IRS or the filers themselves. We discuss some of these issues in our [documentation](https://github.com/CharityNavigator/irs990/blob/master/docs/explore-database.md).
* **990 data only.** The AWS dataset contains both 990 and 990-EZ filings. As of this version, the toolkit only provides support for 990 filings. 
* **No 2015 data.** The AWS dataset contains data from 2011 through 2015. As of this version, the toolkit only provides support for filings through 2014.
* **As with all complex datasets, there will be flaws, mistakes, and bugs in our database.** Some of these are already known. See the [issues page](https://github.com/CharityNavigator/irs990/issues) for known bugs. If you find something wrong, please [report an issue](https://github.com/CharityNavigator/irs990/issues).

### Change log

* 2017-02-02: Rebuilt quick-start AMI to eliminate error message on startup. Also created an AMI for the large database instance.

## Authors

Code and visualizations: David Bruce Borenstein

Documentation: David Bruce Borenstein and Zach Weinsteiger

Crosswalk between XML and database columns (990): Vince Bogucki

Crosswalk between XML and database columns (EZ): David Bruce Borenstein and Zach Weinsteiger
