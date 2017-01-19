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
   1. Increase "Size" to 50 GiB and press "Review and Launch."
   1. Confirm the details and press "Launch."
   1. Create a [key pair](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) (if needed) or choose an existing key pair (returning users). You should end up with a .pem file that functions like a password for the purpose of accessing your new virtual computer.
1. Connect to your virtual computer.
   1. Log into your machine using the instructions that follow. The default username for Amazon Linux is `ec2-user`. [[Windows instructions]](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html) [[Mac/Linux instructions]](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html) 
   
## Process (large database)


* Put an explanation of what our database is all about
* Put an explanation of what MySQL is
* Explain that this tutorial will create an instance inside an RDS instance, which incurs a cost
* Mention that this can also be done on a local MySQL instance
* Ask for feedback about any issues
* Provide steps for cloning the database into RDS

## Notice

*Copyright 2017 Charity Navigator.*

*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*
