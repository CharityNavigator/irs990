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

from base import Base
from util import findWithNa
from util import getNodeOrNone
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

def iii(lookup, filing):
    roots = lookup.getRoots("part_iii")
    ret = []

    for root in roots:
        e = PartIII()
        e.filing = filing
        e.Description =  lookup.findWithNa("part_iii", "Description", root)
        e.ExpenseAmt  =  lookup.findWithNa("part_iii", "ExpenseAmt", root)
        e.GrantAmt    =  lookup.findWithNa("part_iii", "GrantAmt", root)
        e.RevenueAmt  =  lookup.findWithNa("part_iii", "RevenueAmt", root)
        ret.append(e)

    return ret

class PartIII(Base):
    __tablename__ = "part_iii"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    Description = db.Column(db.Text)
    ExpenseAmt = db.Column(db.Numeric(15,2))
    GrantAmt = db.Column(db.Numeric(15,2))
    RevenueAmt = db.Column(db.Numeric(15, 2))

    filing = relationship(Filing)
