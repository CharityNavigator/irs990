# IRS 990 Toolkit v0.1.0

This repository contains tools and instructions for exploring the IRS 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/), offered free to the public by [Charity Navigator](https://www.charitynavigator.org/).

The IRS 990 dataset consists of more than a million individual files. The encoding scheme for these files varies from case to case, and the file structure alone makes them very difficult to retrieve. The tools offered here are intended to facilitate retrieval, comprehension and analysis.

## Prerequisites

At the moment, these tools assume that you have at least a passing familiarity with Amazon Web Services and the Linux command line. Also, you must be willing to spend several dollars (or more) to set up your database. The software we are providing is free; Amazon Web Services is not.

## Limitations

The AWS dataset contains both 990 and 990-EZ filings. As of v0.1.0, the toolkit only provides support for 990 filings. Also, note that there may be flaws, mistakes, and bugs in our database. If you find something wrong, please [report an issue](https://github.com/CharityNavigator/irs990/issues).

## Getting started

## Building a database

 * The easiest, cheapest way to get started is to clone a copy of the IRS database from our S3 mirror. [Instructions](http://placeholder/)
 * If our files are out of date, or if you wish to customize your database, please follow our tutorial for building the database from scratch. [Instructions](http://placeholder/)

### Exploring the schema

If you're just getting started with the AWS 990 dataset, you may wish to explore the structure of the data. We are building a tool for visualizing and exploring the dataset at a high level. The tool is currently being built from the ground up. If you are interested in a preview of the visualization tool, please [mailto:dborenstein@charitynavigator.org] contact us.

*Copyright (c) 2017 Charity Navigator.*

*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*
