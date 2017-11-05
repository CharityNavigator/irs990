# This repo is (mostly) obsolete!

Work on this repo stopped in order to shift to the [`990_long`](https://github.com/CharityNavigator/990_long) repo. In general, `990_long` is more likely to be more useful to you: it has data for every field in every version of the 990, rather than a select handful, as in this repo. On the other hand, this repo preserves the structure of the data, whereas `990_long` transforms the 990 data set into hundreds of millions of key-value pairs.

# IRS 990 Toolkit

This repository contains everything you need to get started exploring the IRS 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/). This includes instructions for an easier-to-use 990 database provided free to the public by [Charity Navigator](https://www.charitynavigator.org/).

## Documentation

To get started, try our [Quick Start](http://990.charitynavigator.org/quick-start). For detailed documentation, see the [project page](http://990.charitynavigator.org).

## File index

The repository contains the code used to build the database from scratch. **Most users should not worry about this at all and instead use the [Quick Start](http://990.charitynavigator.org/quick-start).** For developers, the code is structured as follows:

* **Build scripts:** The database is built in four distinct stages: creation, loading, parsing, and dumping. You can understand the exact process by which the database is built by reading these scripts (in order). If anything is unclear, please [email David Borenstein](mailto:dborenstein@charitynavigator.org).
 * **Creation** (`create_990_database.sh`): Create database and tables; load crosswalk files used to convert the XML e-filings into relational database rows.
 * **Loading** (`load_990_database.sh`): Pull 990 records from Amazon Web Services and into the database.
 * **Parsing** (`parse_990_database.sh`): Extract specific data from each 990 record and load the extracted values into the database.
 * **Dumping** (`dump_990_database.sh`): Create `.sql` files containing your newly generated database.
* **Python code:** The directories `extraction`, `schema`, and `setup` contain the code involved in initializing, then populating, the database. To follow the exact sequence of initialization, look through the build scripts above.
* **SQL code:** The directory `sql` contains very little code, since most of the data tables are generated dynamically using [SQLAlchemy](http://www.sqlalchemy.org/). One exception is the `xml` table. This table is stored in a compressed format, which is hard to set up using SQLAlchemy. 
* **Documentation:** Jekyll markdown for the [documentation website](http://990.charitynavigator.org) is contained in the `docs` folder.

## License

*Copyright (c) 2017 Charity Navigator.*

*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*
