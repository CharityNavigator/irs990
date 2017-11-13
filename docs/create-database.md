## Why you shouldn't use these steps

We have packaged up an image of our database for your convenience and safety. **You probably don't need to build one from scratch.** However, if you want to modify our database or build a newer one than the version that we have posted, we have provided step-by-step instructions for doing so below.

## Why you might need these steps

If you want to add new fields to the database or build a newer one than the version that we have posted, you will need these steps.

## Warning

**The following steps involve creating several virtual computers in the cloud. Every single one of them will be billed by the hour until you shut them off. They will need to run for longer, increasing the total cost of the project. Most importantly, they will be vulnerable to hacking unless you take additional steps to secure them. Please only do this if you know what you're doing.**

## Feedback and pull requests welcome

This project is intended as a launching point for collaborative development on tools for the IRS 990. Our goal was to get something to the community as quickly as possible, in order to encourage feedback and begin an improvement process.

If you are using this project and find the need to extend or modify it, we encourage you to document your changes and create a pull request. If you have a feature that you need help building, please [email the project lead](mailto:dborenstein@charitynavigator.org) about a collaboration.

*On a personal note, this project was my first foray into Spark, and my first non-trivial project using Amazon Web Services. I suspect that I will look back on it with a mixture of pride and embarassment. (See [David Robinson and Hadley Wickham](http://varianceexplained.org/programming/bad-code/)'s argument about the importance of writing bad code.) Why Spark? Two reasons: first, it provided cheap parallelism; and second, it provided an expandable platform for more complicated analyses. --David Borenstein*

## Support for these steps is limited

The following steps are for an advanced audience. The instructions were created as much for in-house use as for public consumption. As such, while we would be happy to discuss them and provide reasonable assistance, please understand that we can only provide so much help. There are a lot of resources you can use to teach yourself any of the steps here. That's how we did it.

## Overview

### Technologies involved

You'll be using three (well, maybe four) AWS services:

* S3, which is a data storage service. The IRS has the raw data here.
* EMR, which allows you to run several computers as a "cluster," which is like a single meta-computer. The underlying technology is called "map-reduce," which is what companies like Google use to make incredibly complicated things happen in an instant. 
* EMR is powered by EC2, which is another Amazon service that lets you rent computers of nearly any size, by the hour. These computers are accessed over the Internet.
* RDS, which is a database rental service that is also priced by the hour. It turns out that RDS is also powered by EC2, but it's less visible to you than it is with EMR.

### Workflow

We are going to download an index of the 990 filings from the internet and store it in a database. We will download all of the filings that we're interested in and store them raw in our database as well. From each filing, we will pull out the version number, which tells us which set of rules to use in order to read it, and store that information in the database. Finally, we will use the correct set of rules to pull out all the informationt that we care about and organize it within the database for easy access. Optionally, now that we have our processed data, we will delete the raw filings to save space and make our database run faster. 

### This is a high level summary

I am assuming that you can figure out how to navigate the menus of the AWS console. Some familiarity with AWS will definitely help here.

## Starting up EMR

### Create an EC2 key pair

EC2 keys are what allow you to gain access to cloud computers that you create. This includes the computers that power the EMR cluster that you'll use for this analysis. The private key is a file that acts like a password, and *it can only be generated once.* This means that, **if you lose it, you will never be able to access your EC2 instance again.** Do not lose it. [[Amazon's instructions for making EC2 Key Pairs.]](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

### Create your EMR cluster

**This will incur significant hourly costs until you turn it off! Do not start until you're ready to follow through!**

Your EMR cluster will do all the work involved in analyzing the 990 data. You'll use an on-demand `m4.xlarge` master node, an on-demand `m4.2xlarge` core node, and five `m4.4xlarge` task nodes to get this whole thing done in a couple of hours.

* Go to the EMR console and click "Create cluster." 
* Click on "Go to advanced options." 
* Under software configuration, check the boxes for Spark and Ganglia. Leave the defaults checked as well.
* Under "edit software settings (optional)," copy and paste `classification=spark-defaults,properties=[maximizeResourceAllocation=true,spark.shuffle.io.maxRetries=9]`
* On the next page, choose the following instance types and counts:
   * Master: One m4.xlarge (on-demand) 
   * Core: Two m4.2xlarge (on-demand)
   * Task: Five (or more) m4.4xlarge (spot). You can get the current price from the little bubble that pops up, or you can see the price history by from the EC2 tab. I like to bid several cents above current asking so that my machines don't get disrupted. It's still way cheaper than on-demand.
* On the next page, choose a cluster name. Under "bootstrap actions," select "custom action." Choose "Configure and add." Under script location, copy and paste `s3://irs-990-toolkit/bootstrap2.sh`
* On the next page, choose the EC2 pair you created. Leave evrything else default.
* Click "create cluster."
* It will take about 15 minutes for your cluster to change from "starting" to "waiting," at which point you can use it.

### Modify security group for your EMR cluster

By default, your EMR master node can't pull the 990 data processing code from GitHub, which you need it to be able to do. You also can't log into it directly, which you'll also need to be able to do. So we're going to explicitly authorize GitHub to send data to EMR master nodes by default, and we're going to open up the cluster for SSH access. You only need to do this once. If you run this code again, you don't need to mess with it.

* Go to the EC2 console.
* Click on "Security Groups."
* Find the security group called `ElasticMapReduce-master.` Click on it.
* Click "Add rule." Where it says "Custom TCP rule," click the drop down and choose "SSH." Where it says "Custom," click the drop down and choose "Anywhere."
* Create additional rules allowing inbound traffic for ports 443, 9418, and 80 from 192.30.252.0/22 (Github).

Again, if you've done this before, you don't need to do it again.

## Starting up RDS

### Create a security group for RDS

By default, your RDS database is not allowed to talk to the computers in your EMR cluster. To give it permission, we create what's called a "security group," which specifies the conditions under which data can move across the database's firewall in either direction. Specifically, we are going to allow inbound access for computers in your EMR cluster. If this is your first time using EMR, you have to do this *after* turning on your first EMR cluster.

To do this, go to the EC2 console and choose "security groups." You wil see a table of security groups. You'll see one called `ElasticMapReduce-master` and another called `ElasticMapReduce-slave`. Next to each of these names is a group ID. Copy and paste these two group IDs into a text editor. Now click "Create security group." Under "Inbound," click "add rule." Set port range to 3306. Under "source," put the group ID for `ElasticMapReduce-master`. Repeat for slave. Choose a recognizable name and hit OK. 

### Create a parameter group for RDS

By default, RDS has settings that will cause our pipeline to crash. The main issue is a failsafe designed to shut down any process that tries to transmit excessive amounts of data in a single transaction. That is exactly what we need to do when we are uploading 990s in XML format, so we shut this failsafe off. The rest of these, to be honest, I can't remember why I changed them; I am embarassed to admit that I made these changes some months ago and did not write down my rationale. I think the timeout ones had to do with transfer of very large pieces of data, but to be honest, I suspect that not all of these are necessary.

Go to the RDS console. On the left is a button called "parameter groups." Click "create parameter group." Under "parameter group family," choose MySQL 5.6. Choose a recognizable name and click "create." Click on your newly created parameter group and then click "edit parameters." For each of the following parameters, search for the parameter name and then set the value to the one shown below. When done, click "Save changes."

* `net_write_timeout` = 600
* `net_read_timeout` = 600
* `max_allowed_packet` = 1073741824
* `innodb_log_file_size` = 1342177280
* `wait_timeout` = 600
 
### Create your RDS database

**This will incur significant hourly costs until you turn it off! Do not start until you're ready to follow through!**

We will now provision (rent) a database instance. Go to the RDS console and click "launch database instance." Choose "MySQL," then "Dev/Test." 

On the main settings page:
* Under DB instance class, choose `db.r3.4xlarge.` Yes, that would cost a fortune if you left it running for a month. Fortunately, you won't do that--see below.
* Disable multi-AZ deployment.
* Allocate 200GB of storage. 
* The instance identifier is how this server will show up on your RDS console. Choose a name you'll recognize.
* The master username and password are how you'll log into the database. (You can also create other usernames and passwords if you're so inclined, but I'm not covering that here.) Write down what you choose, and make it easy to type at the command line--i.e., exclude punctuation.

On the advanced settings page:
* Under VPC security group, choose the security group that you created before.
* Under "DB Parameter group," choose the parameter group you created.
* Leave "Database name" blank. You will deal with that later.
* Launch the instance.
* It will take about 5 minutes for your database's status to become "available."
* When the database is available, copy and paste the `endpoint` value to a text editor. It appears in several locations; depending where you find it, it may or may not end in `:3306`. If it does, delete these five characters or they will mess you up later.

## Running your code

Make sure your EMR instance is "waiting" (~15 minutes from creation) and your RDS instance is "available" (~5 minutes from creation). 

### SSH into the master node

You'll need a way to SSH into your node. If you're working from a Mac or Linux (or Windows 10, which has an Ubuntu command line), you can just type `ssh -i my-private-key.pem hadoop@111.222.333.444`, where `my-private-key.pem` is the key file you created, and `111.222.333.444` is the public IP address of your master node. (The `hadoop` username is a constant--that is what you MUST use.) If you're working from a Windows computer without the Ubuntu console, you'll want to use a tool like PuTTY or MobaXterm to do the equivalent.

Once you're in, you'll need to run a few commands to get the system set up. Type the following:

```
sudo yum -y install git
git clone https://github.com/CharityNavigator/irs990
cd irs990/python
zip ../dependencies.zip *.py
cd ..
```

I also like to install two more programs, `tmux` (which lets you divide your screen into windows) and `htop` (which lets you monitor resource utilization), though it's not necessary:
```
sudo yum -y install htop tmux
```

### Run through steps

After all that prep, this is the easy part. You run the code by running three required steps. From the `irs990` directory, you first run the following:

```
nohup sh create_990_database.sh [endpoint] [username] [password] --prod > out 2> err &
tail -f err
```

Where `[endpoint]`, `[username]`, and `[password]` are, respectively, your RDS instance's endpoint, master username, and master password. If you want to run in test mode (only 1000 filings per year), leave off `--prod`. The arguments must be in this exact order.

This starts the process in a way that doesn't fail if you get disconnected, and then monitors the output.  When it finishes successfully, it's time for the next step.

```
nohup sh load_990_database.sh [endpoint] [username] [password] > out 2> err &
tail -f err
```

Same drill here. In this case, you can tell it's done when it says "shutdown hook called" and then stops doing anything else, and you didn't get any errors in the process. I should probably have added a logging message that tells you when it's totally done. But you can also tell by typing `yarn application -list`. If it doesn't have anything in the list, your program is no longer running. If you didn't get an error message anywhere in your log, everything worked.

Then you can do the last required step:

```
nohup sh parse_990_database.sh [endpoint] [username] [password] > out 2> err &
tail -f err
```

Once this is done, your database is finished. You can do zero, one, or both of two additional optional steps: export the data to file using `dump_990_database.sh` (if you have the disk space for it), and/or remove the XML table from the database now that you no longer need it. That will make your RDS database much faster, because it no longer has this enormous table to contend with. It will also allow you to run the database much more cheaply (i.e., with a much smaller instance type). To do this, you type:

```
mysql -h [endpoint] -P 3306 -u [username] -p[password]
use irs990;
drop table xml;
```

Note the absence of a space between `-p` and your password.

### SHUT DOWN YOUR EMR CLUSTER

Your EMR cluster is costing you several dollars per hour. You're done with it. Shut it down NOW. Go to the EMR console, select your cluster, and choose "Terminate." You may need to disable termination protection.

### Change the database instance type

You can't stop RDS databases indefinitely. You can stop them for up to a week, halting per-hour charges (but not storage charges). The machine will turn back on *automatically* after a week. You may be surprised by your bill if you forget about it.

To avoid that unpleasantness, *resize your machine now*. Go to the RDS console, select your machine, and choose "modify" from the "Instance actions" menu. Choose the smallest instance type (db.t2.micro) and check "Apply immediately." Now you'll be incurring only pennies per hour if you leave the database lying around. When you're ready to use it, crank it up to `db.m3.2xlarge` (if you dropped the XML table) or `db.r3.4xlarge` (if you did not).
