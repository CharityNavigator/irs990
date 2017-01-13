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

class PartVIII(Base):
    __tablename__ = "part_viii"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))

    FedCmpsAmt = db.Column(db.Numeric(15,2))
    MemDuesAmt = db.Column(db.Numeric(15,2))
    FundrAmt = db.Column(db.Numeric(15,2))
    RelOrgAmt = db.Column(db.Numeric(15,2))
    GovGrntAmt = db.Column(db.Numeric(15,2))
    OtherCntAmt = db.Column(db.Numeric(15,2))
    NoncashAmt = db.Column(db.Numeric(15,2))
    TtlCntAmt = db.Column(db.Numeric(15,2))
    TtlPrgRevAmt = db.Column(db.Numeric(15,2))
    CntRptFndAmt = db.Column(db.Numeric(15,2))
    FndGrossAmt = db.Column(db.Numeric(15,2))
    FndDirExpAmt = db.Column(db.Numeric(15,2))
    TtlFndRevAmt = db.Column(db.Numeric(15,2))
    TtlRevAmt = db.Column(db.Numeric(15,2))

    filing = relationship(Filing)
    
    def __init__(self, lookup, filing):
        self.filing       = filing
        self.FedCmpsAmt   = lookup.findWithNa("part_viii", "FedCmpsAmt")
        self.MemDuesAmt   = lookup.findWithNa("part_viii", "MemDuesAmt")
        self.FundrAmt     = lookup.findWithNa("part_viii", "FundrAmt")
        self.RelOrgAmt    = lookup.findWithNa("part_viii", "RelOrgAmt")
        self.GovGrntAmt   = lookup.findWithNa("part_viii", "GovGrntAmt")
        self.OtherCntAmt  = lookup.findWithNa("part_viii", "OtherCntAmt")
        self.NoncashAmt   = lookup.findWithNa("part_viii", "NoncashAmt")
        self.TtlCntAmt    = lookup.findWithNa("part_viii", "TtlCntAmt")
        self.TtlPrgRevAmt = lookup.findWithNa("part_viii", "TtlPrgRevAmt")
        self.CntRptFndAmt = lookup.findWithNa("part_viii", "CntRptFndAmt")
        self.FndGrossAmt  = lookup.findWithNa("part_viii", "FndGrossAmt")
        self.FndDirExpAmt = lookup.findWithNa("part_viii", "FndDirExpAmt")
        self.TtlFndRevAmt = lookup.findWithNa("part_viii", "TtlFndRevAmt")
        self.TtlRevAmt    = lookup.findWithNa("part_viii", "TtlRevAmt")
