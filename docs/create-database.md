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

## Instructions

1. Log into AWS
  1. Create account if needed
  1. Log into AWS
1. Creating a Spark EMR cluster
   1. Create an EC2 key pair (download key!)
   1. Create an EMR Spark cluster (this will cost $)
     1. Give a name such as "990-database-load"
     1. Under "Software configuration," choose the one that starts "Spark." As of this writing, it says "Spark: Spark 2.0.2 on Hadoop 2.7.3 YARN with Ganglia 3.7.2 and Zeppelin 0.6.2." But the versions will change over time.
     1. Default hardware configuration is fine.
     1. Choose the key pair you created.
     1. Click "Create cluster."
     1. Cluster will take about 15 minutes to start.
1. Create RDS (do while cluster is starting)
   1. Go to RDS menu
   1. Select MySQL engine
   1. Choose an m4.xlarge instance and provision 30gb of storage
   1. Under "advanced settings," leave all blank
1. Enable inbound traffic from SSH (for terminal) and a couple other things (for Github) on EMR master node
   1. Go to EMR console on AWS
   1. Click "cluster list"
   1. Go to the cluster you made and click "view cluster details"
   1. On the right, it says "Security groups for Master" and then there's a link. Click the link.
   1. If you see multiple options, click the one with the "Group ID" matching the text in the link from the previous page.
   1. On the bottom of the screen, navigate to the "Inbound" tab.
   1. Click "Edit."
   1. Click "Add rule." Where it says "Custom TCP rule," click the drop down and choose "SSH." Where it says "Custom," click the drop down and choose "Anywhere."
   1. Create additional rules allowing inbound traffic for ports 443, 9418, and 80 from 192.30.252.0/22 (Github).
1. Enable communication between your RDS instance and your EMR instance
   1. Basically, you want to follow [these steps](https://aws.amazon.com/premiumsupport/knowledge-center/rds-cannot-connect/). You want your RDS to allow inbound traffic over port 3306 from members of either the EMR master or slave security groups. 
1. Create an IAM access key
   1. Downloading from S3 costs money. Not much, but to do it, you have to authenticate as yourself. When doing this programatically, we use random sequences of characters called keys. Follow [these instructions](http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) to create a key. Be sure to write down your secret code, as you will never be able to view it again.
1. Connect to your EMR instance
   1. Go to the EC2 console
   1. Click on the instances you have running until you see the one whose security group is called `ElasticMapReduce-master`. Copy the Public IP address into your clipboard.
   1. From Linux or Mac, type `ssh -i my-ec2-key.pem hadoop@1.2.3.4`, where `my-ec2-key.pem` is the EC2 key you created and downloaded earlier, and `1.2.3.4` is the IP address of your master node. (Note to self: provide a link to Windows instructions -DBB)
   1. Acknowledge and accept the security warning, if any.
1. Verify that you configured everything correctly,
   1. Verify that you chose the right kind of EMR cluster by typing `spark-submit --help` and pressing enter. If you get an error, terminate the EMR cluster and make a new one with the right configuration. (See above.)
   1. Verify that you can connect to your RDS instance. Go to the RDS console, click on the RDS instance you created for this project, and copy the endpoint (except the `:3306` at the end) to your clipboard. Type `mysql -h my-endpoint-name -P 3306 -u my-root-name -p`, where `my-endpoint-name` is what's on your clipboard and `my-root-name` is the name of the root user you created for the database. Type your root password. If you get right to a MySQL prompt, you did everything correctly. If it hangs for a long time and then times out, your security groups are still messed up. 
1. Initialize your environment to build the database
   1. Type `sudo yum install git` and wait for git to install.
   1. Type `sudo pip install sqlalchemy` and wait for SQLAlchemy to install.
   1. Clone this repository from github by typing `git clone https://github.com/CharityNavigator/irs990` 
   1. Add the line `export PYTHONPATH=/home/hadoop/irs990` to your `.bash_profile` file. Then run `source .bash_profile`.
   1. Create a `.boto` file with your access key and secret key (Note to self: provide instructions on how to do this)
1. Run the code
   1. Run 'cd irs990`.
   1. Run `sh create_990_database.sh my-endpoint-name my-database-username my-database-password`, where my-endpoint-name and so on are as above. This will _configure_ the database.
   1. Run `sh load_990_database.sh my-endpoint-name my-database-username my-database-password`, where my-endpoint-name and so on are as above. This will download data from S3.
   1. Run `sh parse_990_database.sh my-endpoint-name my-database-username my-database-password`, where my-endpoint-name and so on are as above. This will _populate_ the database.  
1. Shut down your EMR cluster immediately
   1. The EMR cluster is now no longer needed and is running up a hefty bill. Shut it down immediately unless you have plans that involve it.
   1. Once you shut down your EMR cluster, you will no longer have any way of logging into your database (if you followed the steps above). Modify the security group for your RDS to allow traffic from another, less expensive, computer.
1. Use your database, or dump it to .sql, then shut it down
   1. Your SQL instance will continue to incur costs until you shut it down.

