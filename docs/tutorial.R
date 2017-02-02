# This file contains the text of the tutorial that appears when you follow our
# quick-start instructions. These instructions can be found at:
#
#    http://990.charitynavigator.org/quick-start
#
# If you have any issues, please contact David Borenstein:
#
#    dborenstein@charitynavigator.org

# Copyright 2017 Charity Navigator.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#####################
# What's in the box #
#####################

# This AMI contains everything you need to begin exploring IRS 990 data. The AMI
# is based on the RStudio AMI by Louis Aslett:
#
#    http://www.louisaslett.com/RStudio_AMI/
#
# Charity Navigator then pre-loaded the following:
#
#    - An instance of MySQL server
#    - A copy of the Charity Navigator IRS 990 Toolkit database
#    - Necessary R packages (including dev versions for some):
#         install.packages("devtools")
#         devtools::install_github("rstats-db/DBI")
#         devtools::install_github("rstats-db/RMySQL")
#         install.packages("tidyverse")

###################
# Getting started #
###################

### Prerequisites ###

# We assume that you are familiar with the R programming language, and with
# reading documentation for R packages. We also assume that you know what a
# relational database is.
#
# These examples use syntax from the "tidyverse" suite of R packages. 
# We highly recommend using these for all of your R work. If you are not
# familiar with tidyverse, please have a look at:
#
#    https://blog.rstudio.org/2016/09/15/tidyverse-1-0-0/

### Setting up ###

# We highly recommend that you change your RStudio password. Click on
# "Welcome.R" in the upper right and follow the steps there to change the
# password, set up Dropbox, and more.

# Once you've done that, load the required R libraries in order to start
# the tutorial by running the following lines.
library(RMySQL)
library(tidyverse)

### Querying the database ###

# The following line will give you a list of the tables in the database.
src_mysql("irs990", password = "load990")

# You can look at the top of a table using the "tbl" command from dplyr.
src_mysql("irs990", password = "load990") %>%
  tbl("filing")

# Let's look at the number of 990s by tax period. Note that, as of this preview
# version, tax periods are reported as ending on the first day of the month;
# they should actually be reported as ending on the last day of the month.
src_mysql("irs990", password = "load990") %>%
  tbl("filing") %>%
  group_by(TaxPeriod) %>%
  summarise(n = n()) %>%
  ungroup()

# Now let's get the same thing by year. We have to use the "collect()" statement to
# load all the data before we can use most logic. See the dplyr databases
# vignette for more: 
#
#    https://cran.r-project.org/web/packages/dplyr/vignettes/databases.html
#
src_mysql("irs990", password = "load990") %>%
  tbl("filing") %>%
  collect(n = Inf) %>%
  mutate(y = lubridate::year(TaxPeriod)) %>%
  group_by(y) %>%
  summarise(n = n()) %>%
  ungroup()

# We can get the same information from the header. Let's do a sanity check--
# and see just how messy these data are.
db <- src_mysql("irs990", password = "load990") 

header <- db %>% 
  tbl("header")

filing <- db %>% 
  tbl("filing")

year_check <- left_join(header, filing, by=c("FilingId" = "id")) %>%
  group_by(TaxPeriod, TaxYr) %>%
  summarise(n = n()) %>%
  ungroup() %>%
  arrange(TaxYr, TaxPeriod) %>%
  collect()

# Let's get a histogram of revenue.
part_i <- db %>%
  tbl("part_i") %>%
  collect(n = Inf)

ggplot(part_i, aes(x=Revenue)) +
  geom_histogram(bins=1000) +
  scale_x_log10(label = scales::dollar) +
  scale_y_continuous(label = scales::comma)

# We can also break this out by tax year.
rev_tax_yr <- left_join(tbl(db, "part_i"), tbl(db, "header"), by = "FilingId") %>%
  select(TaxYr, Revenue) %>%
  collect(n = Inf)

ggplot(rev_tax_yr, aes(x=Revenue)) +
  geom_histogram(bins=1000) +
  scale_x_log10(label = scales::dollar) +
  scale_y_continuous(label = scales::comma) +
  facet_wrap(~ TaxYr)

# Next, let's do a regression of organization age and revenue.
rev_age <- left_join(tbl(db, "part_i"), tbl(db, "header"), by = "FilingId") %>%
  select(FormYr, TaxYr, Revenue) %>%
  collect(n = Inf) %>%
  mutate(age = TaxYr - FormYr) %>%
  filter(age >= 0) %>% # Get rid of cases where year formed is after tax year
  filter(!is.na(age)) %>%
  filter(!is.na(RevLessExp))

# It's highly significant. Is it a good fit?
lm(Revenue ~ age, data = rev_age) %>% summary()

# It's a terrible fit, but there's so much data that we still get signal.
ggplot(rev_age, aes(x = age, y = Revenue)) +
  geom_smooth(method = "lm") +
  geom_point(size = 0, alpha = 0.1)

# Finally, therefore, let's how likely you are to operate at a loss as a function
# of years in operation.
loss_age <- left_join(tbl(db, "part_i"), tbl(db, "header"), by = "FilingId") %>%
  select(FormYr, TaxYr, Revenue) %>%
  collect(n = Inf) %>%
  mutate(age = TaxYr - FormYr) %>%
  filter(age >= 0) %>% # Get rid of cases where year formed is after tax year
  filter(!is.na(age)) %>%
  filter(!is.na(Revenue)) %>%
  mutate(is_loss = Revenue < 0) %>%
  group_by(age) %>%
  summarise(n_tot = n(), n_loss = sum(is_loss)) %>%
  ungroup() %>%
  mutate(frac_loss = n_loss / n_tot)

# There are hints that it peaks around 15 years and then plateaus, which makes
# sense. We would have to do more to see if it's real.
ggplot(loss_age, aes(x = age, y = frac_loss)) +
  geom_point()

# This concludes our quick tutorial. We are open to suggestions about additional
# examples and exercises. Please drop us a line, and we will be glad to discuss!
#
#     Project lead: David Bruce Borenstein, PhD
#                   dborenstein@charitynavigator.org
