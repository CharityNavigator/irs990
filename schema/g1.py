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
from util import getNodeOrNone
from base import Base
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

def g1(lookup, filing):
    roots = lookup.getRoots("sched_g_part_i")
    ret = []

    for root in roots:
        e = ScheduleGPartI()
        e.filing = filing
        e.PersonNm       = lookup.findWithNa("sched_g_part_i","PersonNm",root)
        e.BusinessNm1    = lookup.findWithNa("sched_g_part_i","BusinessNm1",root)
        e.BusinessNm2    = lookup.findWithNa("sched_g_part_i","BusinessNm2",root)
        e.ActivityTxt    = lookup.findWithNa("sched_g_part_i","ActivityTxt",root)
        e.FndControl     = lookup.findTrueFalse("sched_g_part_i","FndControl",root)
        e.GrsRcptAmt     = lookup.findWithNa("sched_g_part_i","GrsRcptAmt",root)
        e.ContractAmt    = lookup.findWithNa("sched_g_part_i","ContractAmt",root)
        e.OrgNetAmt      = lookup.findWithNa("sched_g_part_i","OrgNetAmt",root)
        ret.append(e)

    return ret

class ScheduleGPartI(Base):
    __tablename__ = "sched_g_part_i"
    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    PersonNm = db.Column(db.String(255))
    BusinessNm1 = db.Column(db.String(255))
    BusinessNm2 = db.Column(db.String(255))
    ActivityTxt = db.Column(db.Text)
    FndControl = db.Column(db.Boolean)
    GrsRcptAmt = db.Column(db.Numeric(15,2))
    ContractAmt = db.Column(db.Numeric(15,2))
    OrgNetAmt = db.Column(db.Numeric(15,2))
    filing = relationship(Filing)
