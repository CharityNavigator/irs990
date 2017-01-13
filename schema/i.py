from schema.lookup.single import SingletonLookup
from base import Base
from filing import Filing
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship

class PartI(Base):
    __tablename__ = "part_i"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    VoteBodyCount = db.Column(db.Integer)
    Revenue = db.Column(db.Integer)
    Expenses = db.Column(db.Integer)
    RevLessExp = db.Column(db.Integer)

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing = filing
        self.VoteBodyCount = lookup.findWithNa("part_i", "VoteBodyCount")
        self.VoteIndpCount = lookup.findWithNa("part_i", "VoteIndpCount")
        self.Revenue       = lookup.findWithNa("part_i", "Revenue")
        self.Expenses      = lookup.findWithNa("part_i", "Expenses")
        self.RevLessExp    = lookup.findWithNa("part_i", "RevLessExp")
