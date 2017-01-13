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

class PartX(Base):
    __tablename__ = "part_x"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))

    TtlRevEOYAmt = db.Column(db.Numeric(15,2))
    TtlLblEOYAmt = db.Column(db.Numeric(15,2))
    UnrAssEOYAmt = db.Column(db.Numeric(15,2))
    TmpRstAssEOYAmt = db.Column(db.Numeric(15,2))
    PrmRstAssEOYAmt = db.Column(db.Numeric(15,2))
    CapStkTrEOY = db.Column(db.Numeric(15,2))
    PtInCapEOYAmt = db.Column(db.Numeric(15,2))
    RtnEndEOYAmt = db.Column(db.Numeric(15,2))
    TtlNetEOYAmt = db.Column(db.Numeric(15,2))
    SFAS117Yes = db.Column(db.Boolean)
    SFAS117No = db.Column(db.Boolean)

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing          = filing
        self.TtlRevEOYAmt    = lookup.findWithNa("part_x","TtlRevEOYAmt")
        self.TtlLblEOYAmt    = lookup.findWithNa("part_x","TtlLblEOYAmt")
        self.UnrAssEOYAmt    = lookup.findWithNa("part_x","UnrAssEOYAmt")
        self.TmpRstAssEOYAmt = lookup.findWithNa("part_x","TmpRstAssEOYAmt")
        self.PrmRstAssEOYAmt = lookup.findWithNa("part_x","PrmRstAssEOYAmt")
        self.CapStkTrEOYAmt  = lookup.findWithNa("part_x","CapStkTrEOYAmt")
        self.PtInCapEOYAmt   = lookup.findWithNa("part_x","PtInCapEOYAmt")
        self.RtnEndEOYAmt    = lookup.findWithNa("part_x","RtnEndEOYAmt")
        self.TtlNetEOYAmt    = lookup.findWithNa("part_x","TtlNetEOYAmt")
        self.SFAS117Yes      = lookup.findTrueFalse("part_x","SFAS117Yes")
        self.SFAS117No       = lookup.findTrueFalse("part_x","SFAS117No")
