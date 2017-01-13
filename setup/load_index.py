# Copyright 2017 Charity Navigator.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from schema import *
import boto
from boto.s3.key import Key

cred = base.Credentials()
engineStr = cred.getEngineStr()
engine = create_engine(engineStr)

def key_to_str(bucket, key):
    #start = time.time()
    ret = bucket.get_key(key) \
            .get_contents_as_string() \
            .replace("\r", "")
    #end = time.time()
    #print "Retrieved %s in %0.2fs." % (key,end-start)
    return ret

def get_na(record, key):
    if key in record:
        return record[key]
    return None
    
def submittedOn(raw):
    return datetime.strptime(raw, "%Y-%m-%d").date()

def taxPeriod(raw):
    return datetime.strptime(raw, "%Y%m").date()

def lastUpdated(raw):
    raw = raw.split(".")[0]
    return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print "Connecting to S3."
s3 = boto.connect_s3(host="s3.amazonaws.com")
print "Getting 990 bucket."
bucket = s3.get_bucket("irs-form-990")

for year in range(2011, datetime.now().year):
    print("Processing year %i." % year)
    print("  ...retrieving JSON index from Amazon S3.")
    key = "index_%i.json" % (year)
    index_json = key_to_str(bucket, key)
    index = json.loads(index_json)
    print("  ...Decoding JSON index.")
    records = index["Filings%i" % year]
    print("  ...Loading index into database.")
    for record in records:
        f = filing.Filing()
        f.OrganizationName = get_na(record, "OrganizationName")
        f.ObjectId         = get_na(record, "ObjectId")
        f.SubmittedOn      = submittedOn(get_na(record, "SubmittedOn"))
        f.DLN              = get_na(record, "DLN")
        f.LastUpdated      = lastUpdated(get_na(record, "LastUpdated"))
        f.TaxPeriod        = taxPeriod(get_na(record, "TaxPeriod"))
        f.IsElectronic     = get_na(record, "IsElectronic")
        f.IsAvailable      = get_na(record, "IsAvailable")
        f.FormType         = get_na(record, "FormType")
        f.EIN              = get_na(record, "EIN")
        f.URL              = get_na(record, "URL")

        session.add(f)
        session.commit()

session.close()
