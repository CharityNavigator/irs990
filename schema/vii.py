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
from util import getNodeOrNone
from util import findTrueFalse
from base import Base
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

def vii(lookup, filing):
    roots = lookup.getRoots("part_vii_a")
    ret = []

    for root in roots:
        e = PartVIIa()
        e.filing = filing
        e.PersonNm     =  lookup.findWithNa("part_vii_a","PersonNm", root)
        e.TitleTxt     =  lookup.findWithNa("part_vii_a","TitleTxt", root)
        e.AvgHrs       =  lookup.findWithNa("part_vii_a","AvgHrs", root)
        e.AvgHrsRltd   =  lookup.findWithNa("part_vii_a","AvgHrsRltd", root)
        e.TrustOrDir   =  lookup.findTrueFalse("part_vii_a","TrustOrDir", root)
        e.Officer      =  lookup.findTrueFalse("part_vii_a","Officer", root)
        e.KeyEmpl      =  lookup.findTrueFalse("part_vii_a","KeyEmpl", root)
        e.HighComp     =  lookup.findTrueFalse("part_vii_a","HighComp", root)
        e.FmrOfficer   =  lookup.findTrueFalse("part_vii_a","FmrOfficer", root)
        e.RptCmpOrg    =  lookup.findWithNa("part_vii_a","RptCmpOrg", root)
        e.RptCmpRltd   =  lookup.findWithNa("part_vii_a","RptCmpRltd", root)
        e.OtherComp    =  lookup.findWithNa("part_vii_a","OtherComp", root)
        ret.append(e)

    return ret

class PartVIIa(Base):
    __tablename__ = "part_vii_a"
    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    PersonNm = db.Column(db.String(255))
    TitleTxt = db.Column(db.String(255))
    AvgHrs = db.Column(db.Numeric(7,2))
    AvgHrsRltd = db.Column(db.Numeric(7,2))
    TrustOrDir = db.Column(db.Boolean)
    Officer = db.Column(db.Boolean)
    KeyEmpl = db.Column(db.Boolean)
    HighComp = db.Column(db.Boolean)
    FmrOfficer = db.Column(db.Boolean)
    RptCmpOrg = db.Column(db.Numeric(15,2))
    RptCmpRltd = db.Column(db.Numeric(15,2))
    OtherComp = db.Column(db.Numeric(15,2))

    filing = relationship(Filing)
