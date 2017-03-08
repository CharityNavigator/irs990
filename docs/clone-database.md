# Cloning the 990 database into MySQL

## About the 990 database

Charity Navigator depends on the IRS 990 for part of its rating process. The 990 database associated with this toolkit is a first step at leveraging newer, electronic versions of this crucial public record for this purpose. As such, this database captures data relevant to the Charity Navigator rating process. 

## Which version should I use?

Charity Navigator provides **two** versions of the 990 database.

* A small (~3GB) database capturing selected fields from the IRS 990 from tax years 2011 to 2014. 
* A large (~41GB) database capturing the above fields, plus all of the raw 990 data in an indexed and searchable form.

We recommend that you start with the small database for exploring the 990 dataset, which will be cheaper and easier. 

## Prerequisites

Using either the small or the large database requires the ability to use SQL databases, as well as passing familiarity with Linux and Amazon Web Services. You must also be willing to spend money on instantiating the database. Our data are free to use; Amazon Web Services is not. Building the small database should be quite inexpensive if you do it as specified; the large one will run up a bigger bill.

## Set-up process (small database)

1. Create an AWS account (if needed) and log in. See [Amazon's official documentation](https://aws.amazon.com/) for help.
1. Create a virtual computer (EC2 instance) to use for the project. For the small database, you can run everything on this one machine.
   1. Go to the "Services" menu in AWS and choose "EC2."
   1. Click "Launch Instance."
   1. Select "Amazon Linux AMI."
   1. Click on "m4.xlarge" and press "Configure Instance Details." As of this writing, m4.xlarge [costs](https://aws.amazon.com/ec2/pricing/on-demand/) $0.215 per hour.
   1. Accept all the defaults on Step 3 (Configure Instance Details) and continue to "Add Storage."
   1. Increase "Size" to 20 GiB and press "Review and Launch."
   1. Confirm the details and press "Launch."
   1. Create a [key pair](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) (if needed) or choose an existing key pair (returning users). You should end up with a .pem file that functions like a password for the purpose of accessing your new virtual computer.
1. Connect to your virtual computer.
   1. Log into your machine using the instructions that follow. The default username for Amazon Linux is `ec2-user`. [[Windows instructions]](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html) [[Mac/Linux instructions]](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html) 
1. Configure your virtual computer.
   1. Follow [these steps](https://support.rackspace.com/how-to/installing-mysql-server-on-centos/) to install MySQL server, which we will use to run the database.
   1. Run `mysql -u root -pmypassword` where `mypassword` is the password you just set.
   1. Run `CREATE DATABASE irs990;` and then `EXIT`.
   1. If you do not already have one for another reason, [create an AWS access key pair](http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html). This is not the same as the key pair you created earlier. That let you log into the virtual computer; this allows you to authenticate for billing purposes, which you must do in order to download the 990 data.
   1. Run `aws configure` and provide the access key and secret access key. If needed, see the [AWS documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) for more info.
1. Download and set up the database.
   1. Download the latest version of our database image by typing `aws s3 cp s3://irs-990-toolkit/data/irs990_no_xml_2017_03_07.sql.tar.gz .`
   1. The file is compressed for easier transfer. Uncompress it by typing `tar -xvf irs990_no_xml_2017_03_07.sql.tar.gz`
   1. Load the database by typing `mysql -u root -pmypassword irs990 < irs990_no_xml_2017_03_07.sql`, where `mypassword` is the root password you created. This will take about 10 minutes.

## Exploring the dataset

See our [database overview](https://github.com/CharityNavigator/irs990/blob/master/docs/explore-database.md) page for a description of the database's contents.

## Clean-up process (small database)

The database is now ready for use. It is also costing you by the hour. **When you are done with what you need**, therefore, you have two basic options:

* Delete the system by going to the EC2 console, clicking on your virtual machine, then going to `Actions > Instance State > Terminate`. You will not incur any more costs, but you will have to go through these steps whenever you want to use the database.

* Shut down the system by going to the EC2 console, clicking on your virtual machine, then going to `Actions > Instance State > Stop`. You will pay for the 50GiB of storage you provisioned, but nothing else. At the time of this writing, provisioned SSD storage costs $0.10 per GiB-month, or $5.00 per month in this case. To turn your database back on, just go to the EC2 console and choose `Actions > Instance State > Start`.

## If you want to use the large database

In principle, you could use nearly the exact same steps for the large database. The only differences are as follows:
* Use an instance type with more computing power and a lot more memory, such as "r4.2xlarge."
* Provision much more storage space--more like 100 GiB.
* Download and use`irs990_complete_2017_03_07.sql.tar.gz` instead of `irs990_no_xml_2017_03_07.sql.tar.gz`.

In practice, we recommend using separate computers for the database and for your interaction with it. It will run faster and probably end up cheaper. The easiest way to do this is to create an [RDS](https://aws.amazon.com/rds/) instance for your database, which is a managed service for databases. The downside is that this is more complex and, if done wrong, could create security issues (or large server bills), so consult an IT person. 
