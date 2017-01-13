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

from util import findWithNa
from util import findTrueFalse
from base import Base
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

def validateFormYr(y):
    if y == None:
        return None

    try:
        prov = int(y)
        if prov < 1901:
            return None

        if prov > 2017:
            return None

        return prov

    except ValueError:
        return None
class Header(Base):
    __tablename__ = "header"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    FilerEIN = db.Column(m.CHAR(9))
    TaxYr = db.Column(m.YEAR)
    Amended = db.Column(db.Boolean)
    FilerName1 = db.Column(db.String(255))
    FilerName2 = db.Column(db.String(255))
    PdBeginDt = db.Column(db.Date)
    PdEndDt = db.Column(db.Date)
    Org501c3 = db.Column(db.Boolean, nullable=False)
    Org501cInd = db.Column(db.Boolean, nullable=False)
    Org501cType = db.Column(db.String(3))
    Org4947a1 = db.Column(db.Boolean)
    Org527Ind = db.Column(db.Boolean)
    FormYr = db.Column(m.YEAR)

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing      = filing
        self.FilerEIN    = lookup.findWithNa("header","FilerEIN")
        self.TaxYr       = lookup.findWithNa("header","TaxYr")
        self.Amended     = lookup.findTrueFalse("header","Amended")
        self.FilerName1  = lookup.findWithNa("header","FilerName1")
        self.FilerName2  = lookup.findWithNa("header","FilerName2")
        self.PdBeginDt   = lookup.findWithNa("header","PdBeginDt")
        self.PdEndDt     = lookup.findWithNa("header","PdEndDt")
        self.Org501c3    = lookup.findTrueFalse("header","Org501c3")
        self.Org501cInd  = lookup.findTrueFalse("header","Org501cInd")
        self.Org501cType = lookup.getTextAllowingAttribute("header","Org501cType")
        self.Org4947a1   = lookup.findTrueFalse("header","Org4947a1")
        self.Org527Ind   = lookup.findTrueFalse("header","Org527Ind")
        formYr           = lookup.findWithNa("header","FormYr")
        self.FormYr      = validateFormYr(formYr)
