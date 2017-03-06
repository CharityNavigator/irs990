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

def l2(lookup, filing):
    roots = lookup.getRoots("sched_l_part_ii")
    ret = []

    for root in roots:
        e = ScheduleLPartII()
        e.filing = filing
        e.PersonNm       =  lookup.findWithNa("sched_l_part_ii","PersonNm", root)
        e.BusinessNm     =  lookup.findWithNa("sched_l_part_ii","BusinessNm", root)
        e.Relationship   =  lookup.findWithNa("sched_l_part_ii","Relationship", root)
        e.Purpose        =  lookup.findWithNa("sched_l_part_ii","Purpose", root)
        e.ToOrg          =  lookup.findTrueFalse("sched_l_part_ii","ToOrg", root)
        e.FromOrg        =  lookup.findTrueFalse("sched_l_part_ii","FromOrg", root)
        e.OrigPrincipal  =  lookup.findWithNa("sched_l_part_ii","OrigPrincipal", root)
        e.BalanceDue     =  lookup.findWithNa("sched_l_part_ii","BalanceDue", root)
        e.Default        =  lookup.findTrueFalse("sched_l_part_ii","Default", root)
        e.Approved       =  lookup.findTrueFalse("sched_l_part_ii","Approved", root)
        e.Written        =  lookup.findTrueFalse("sched_l_part_ii","Written", root)
        ret.append(e)

    return ret


class ScheduleLPartII(Base):
    __tablename__ = "sched_l_part_ii"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))

    PersonNm = db.Column(db.String(255))
    BusinessNm = db.Column(db.String(255))
    Relationship = db.Column(db.String(255))
    Purpose        = db.Column(db.Text)
    ToOrg          = db.Column(db.Boolean)
    FromOrg        = db.Column(db.Boolean)
    OrigPrincipal  = db.Column(db.Numeric(15,2))
    BalanceDue     = db.Column(db.Numeric(15,2))
    Default        = db.Column(db.Boolean)
    Approved       = db.Column(db.Boolean)
    Written        = db.Column(db.Boolean)
    filing = relationship(Filing)
