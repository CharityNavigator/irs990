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

PARTITIONS = 200

import sys
from lxml import etree
from schema import *
from lookup import SingletonLookup, MultiLookup 
from cred import Credentials
from pyspark import SparkContext
cr = Credentials()

sc = SparkContext()

def append(elements, element):
    if element == None:
        return
    elements.append(element)

def extend(elements, element):
    if element == None:
        return
    elements.extend(element)

def makeSession():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engineStr = cr.getEngineStr()
    engine = create_engine(engineStr)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

# Records are loaded transactionally, so we can ignore anything that has part I
def hasPartOne(filing, session):
    n = session.query(PartI)\
            .filter(PartI.filing == filing)\
            .count()

    return (n > 0)

def parseFilings(filings):
    session = makeSession()
    for filing in filings:
        try:
            if (hasPartOne(filing, session)):
                #print "Skipping filing %s because already processed" % str(filing.id)
                continue
            raw = session.query(RawXML)\
                    .filter(RawXML.filing == filing)[0]

            elements = []
            sLookup = SingletonLookup(session, raw)
            mLookup = MultiLookup(session, raw)
            append(elements, Header(sLookup, filing))
            append(elements, PartI(sLookup, filing))
            extend(elements, iii(mLookup, filing))
            append(elements, PartIV(sLookup, filing))
            append(elements, PartVI(sLookup, filing))
            extend(elements, vii(mLookup, filing))
            append(elements, PartVIII(sLookup, filing))
            append(elements, PartIX(sLookup, filing))
            append(elements, PartX(sLookup, filing))
            append(elements, PartXII(sLookup, filing))
            extend(elements, g1(mLookup, filing))
            extend(elements, l2(mLookup, filing))
            for element in elements:
                session.add(element)
                session.commit()
        
        except:
            session.rollback()
            session.close()
            session = makeSession()
            continue

        session.close()


session = makeSession()
filings = session.query(Filing)\
        .filter(Filing.FormType == "990")\
        .filter(Filing.URL != None)\
        .filter(Filing.raw != None)

session.close()

sc.parallelize(filings, PARTITIONS)\
        .foreachPartition(parseFilings)
