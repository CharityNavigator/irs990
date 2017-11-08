# Code walkthrough

This walkthrough steps through the four build scripts involved in setting up this system. Combined with the [instructions on how to build the database from scratch](http://990.charitynavigator.org/create-database), this should provide all of the documentation necessary to maintain and extend this codebase. This program represents my very first use of Apache Spark, and it shows.

**All of the `.sh` files mentioned are in the root directory of the project.** They each make calls to a series of code files. I am describing what each code file is.

## `create_990_database.sh`

This file creates the structure into which data will be loaded. It runs through each of the following database-related files. It takes as its first, second, and third arguments the hostname, username, and password of your database respectively.

### `./sql/setup_db.sql`

This drops the database `irs990`, if it exists, and then creates it, thereby starting from scratch.

### `./setup/create_db.py`

This file creates all our database tables. Rather than doing it through SQL statements, it uses an object-relational mapping tool called SQLAlchemy. The tables are all defined as Python objects in the `/schema` directory. This file imports each object type and then instructs SQLAlchemy to instantiate a SQL table that can represent it.

### `./sql/create_xml_table.sql`

I wanted the XML table to be compressed, because plain text XML is pretty huge. I was having trouble setting this up in SQLAlchemy, so I instantiate this particular table by hand. This is ugly, I know.

### `./setup/load_990_singletons.py`

The XML file is a hierarchy, and the relational database is a different hierarchy. Consequently, anything for which there can be more than one of it per filing needs to be handled with care if we wish to retain structure. For everything else, we can treat the Xpath as a simple mapping. This step loads those simple mappings, and the following two steps handle the more complex cases. The file that `load_990_singletons.py` reads, `data/990_singletons.csv`, is a simple mapping of fields to Xpaths by 990 version. This is the precursor to the community-developed [concordance](https://github.com/Nonprofit-Open-Data-Collective/irs-efile-master-concordance-file).

### `./setup/load_990_roots.py` and `./setup/load_990_stems.py`

The algorithm I used for handling hierarchical relationships is as follows: Go to a leaf node in the XML schema. Keep going up the tree until you reach a node whose parent has children that map to more than one database table. The Xpath to this node is the root of a group of fields in a one-to-many relation to the filing. The community concordance lacks this concept, because it would have been too difficult to ask volunteers to grasp it. It will need to be added on after the fact.

As their names imply, the `load_990_roots.py` and `load_990_stems.py` load the roots and stems of one-to-many relationships, respectively.

## `load_990_database.sh`

Now that we have our structure set up, we can load in the actual data.

### `./setup/load_index.py`

The IRS 990 dataset consists of three sets of files: `.json` index files, `.csv` index files, and the `xml` files containing the 990s. The `.json` and `.csv` files are interchangeable except that, for some reason, the `.csv` files lack filing URLs. This is actually reasonable once you realize that you can actually infer the URL from the object ID, and that you probably want to pull it directly over S3 instead of over HTTP anyway. At any rate, I used the `.json` files. This script pulls them and uses them to populate the database. It uses `boto`, a Python interface for AWS, to pull the data directly over the S3 protocol. It also uses Spark, but basically only as "easy" parallelism--there's no map-reduce going on here.

### `./extraction/load_xml.py`

Once you have the names of the XML files, you need to pull them. You can't just pull them all at once and iterate through them because the IRS put them all in the same directory, which breaks the `aws s3 ls` and `aws s3 sync` commands. This file goes through the names in the database and pulls their XML into a table in the database. Why bother pulling all the raw XML at once? It lets you open a relatively small number of S3 connections and transfer the data to local storage all at once. Had I known more about Spark, I would have loaded the data into HDFS, which is distributed over all the computers in my cluster, obviating the need for an external database. This is the approach that I took in `990_long`.

## `parse_990_database.sh`

As its name suggests, this script runs steps that go through the XML and extracts information from it.

### `./extraction/parse_version.py`

There are dozens of different versions of the IRS 990 XML schema, and they can potentially have different mappings for the same variable. So this step goes through and identifies the version of each 990, which determines how to process it going forward. (990_long handles this problem more elegantly.)

### `./extraction/parse_body.py`

This script goes through file by file, finds the xpath (or roots and stems) that correspond to each desired field, looks them up, and populates the database with them if they exist. In 990_long, I just crawl the xpath hierarchy and merge it with the variable names--much easier, but lacks the structure of this database. The same principle can be applied to the structured version, though--I plan to implement that soon!
 
## `dump_990_database.sh`

This file does not call out to any other code. It uses a built-in tool from mysql, `mysqldump`, to export two versions of the database: one with just the data, and one with a table containing the raw XML. 
