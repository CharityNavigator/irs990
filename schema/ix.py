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

class PartIX(Base):
    __tablename__ = "part_ix"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))

    GrnDomOrgAmt = db.Column(db.Numeric(15,2))
    GrnDomIndAmt = db.Column(db.Numeric(15,2))
    GrnFrnAmt = db.Column(db.Numeric(15,2))
    FundrFeesAmt = db.Column(db.Numeric(15,2))
    AffilPmtAmt = db.Column(db.Numeric(15,2))
    FncExpTtlAmt = db.Column(db.Numeric(15,2))
    FncExpSvcAmt = db.Column(db.Numeric(15,2))
    FncExpMgtAmt = db.Column(db.Numeric(15,2))
    FncExpFndAmt = db.Column(db.Numeric(15,2))
    JntCstTtlAmt = db.Column(db.Numeric(15,2))
    JntCstSvcAmt = db.Column(db.Numeric(15,2))
    JntCstMgtAmt = db.Column(db.Numeric(15,2))
    JntCstFdrAmt = db.Column(db.Numeric(15,2))

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing       = filing
        self.GrnDomOrgAmt = lookup.findWithNa("part_ix","GrnDomOrgAmt")
        self.GrnDomIndAmt = lookup.findWithNa("part_ix","GrnDomIndAmt")
        self.GrnFrnAmt    = lookup.findWithNa("part_ix","GrnFrnAmt")
        self.FundrFeesAmt = lookup.findWithNa("part_ix","FundrFeesAmt")
        self.AffilPmtAmt  = lookup.findWithNa("part_ix","AffilPmtAmt")
        self.FncExpTtlAmt = lookup.findWithNa("part_ix","FncExpTtlAmt")
        self.FncExpSvcAmt = lookup.findWithNa("part_ix","FncExpSvcAmt")
        self.FncExpMgtAmt = lookup.findWithNa("part_ix","FncExpMgtAmt")
        self.FncExpFndAmt = lookup.findWithNa("part_ix","FncExpFndAmt")
        self.JntCstTtlAmt = lookup.findWithNa("part_ix","JntCstTtlAmt")
        self.JntCstSvcAmt = lookup.findWithNa("part_ix","JntCstSvcAmt")
        self.JntCstMgtAmt = lookup.findWithNa("part_ix","JntCstMgtAmt")
        self.JntCstFdrAmt = lookup.findWithNa("part_ix","JntCstFdrAmt")
