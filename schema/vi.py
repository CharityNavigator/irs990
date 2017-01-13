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

from util import findTrueFalse 
from base import Base
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

class PartVI(Base):
    __tablename__ = "part_vi"
    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))

    Diversion = db.Column(db.Boolean)
    HasMinutes = db.Column(db.Boolean)
    PrvForm990 = db.Column(db.Boolean)
    COIPolicy = db.Column(db.Boolean)
    WBPolicy = db.Column(db.Boolean)
    DocRetPolicy = db.Column(db.Boolean)
    CeoCompProc = db.Column(db.Boolean)

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing       = filing
        self.Diversion    = lookup.findTrueFalse("part_vi", "Diversion")
        self.HasMinutes   = lookup.findTrueFalse("part_vi", "HasMinutes")
        self.PrvForm990   = lookup.findTrueFalse("part_vi", "PrvForm990")
        self.COIPolicy    = lookup.findTrueFalse("part_vi", "COIPolicy")
        self.WBPolicy     = lookup.findTrueFalse("part_vi", "WBPolicy")
        self.DocRetPolicy = lookup.findTrueFalse("part_vi", "DocRetPolicy")
        self.CeoCompProc  = lookup.findTrueFalse("part_vi", "CeoCompProc")
