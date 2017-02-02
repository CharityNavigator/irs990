# Quick start

The easiest way to get started with the toolkit is to create an Amazon EC2 instance with the [your choice of our two databases](http://990.charitynavigator.org/clone-database) and RStudio pre-loaded. The following steps will actually create a website from which you can write code to explore the database. A tutorial will appear on screen as soon as you log in. You can even link it to Dropbox to transfer work in and out.

## Licensing considerations

Our code is licensed under the MIT license, which gives you permission to do anything you want with it as long as you acknowledge us. RStudio uses the [Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) (AGPL), which imposes far more restrictions. The database is loaded onto on MySQL, which uses the [General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) (GPL). If your company does not allow the use of the GPL or AGPL, please use our [database image](http://990.charitynavigator.org/clone-database) instead.

## Instructions

1. Click Follow one of the following two links: 
   * [Small database (no raw 990s)](https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-a86991be)
   * [Large database (can look up raw 990s)](https://placeholder.com)
1. Under "Choose an Instance Type," choose `m4.xlarge` (small database) or `m4.4xlarge` (large database) and hit continue. For higher peformance, consider `c4.2xlarge` and `c4.8xlarge` respectively. This server will incur an hourly charge until you shut it down; see Amazon's [EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/). 
1. Keep clicking "Next" until you get to "Step 6: Configure Security Group."
1. Click "Add rule." Under "Type," choose "HTTP." Click "Review and Launch."
1. Wait about 10 minutes, then go to the [EC2 dashboard](https://console.aws.amazon.com/ec2). The instance you created should show its state as "Running" and have a green circle next to it. If it says "pending," wait longer. (You should wait at least five minutes after it first says "Running.")
1. Click on the instance you just made. Under details, find the "IPv4 Public IP."
1. Copy and paste the public IP address into your web browser. 
1. You should be prompted for a username and password. Type "rstudio" for both, and click "log in." The first time you log in, you may need to wait a few minutes.
1. You should be greeted with an RStudio screen asking you to review the open source license. Scroll down to accept the license and begin the tutorial. You're good to go!
