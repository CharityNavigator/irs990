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

from util import *
import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Crosswalk(Base):
    __tablename__ = "crosswalk"

    id        = db.Column(db.Integer, primary_key=True)
    FormType  = db.Column(db.String(5), nullable=False)
    tbl       = db.Column(db.String(64), nullable=False)
    field     = db.Column(db.String(64), nullable=False)
    version   = db.Column(db.String(20), nullable=False)
    path      = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

# Root paths for group fields in 990.
class Root(Base):
    __tablename__ = "root"

    id          = db.Column(db.Integer, primary_key=True)
    FormType    = db.Column(db.String(5), nullable=False)
    tbl         = db.Column(db.String(64), nullable=False)
    version     = db.Column(db.String(20), nullable=False)
    path        = db.Column(db.String(1000), nullable=False)

# Root stems for group fields in 990.
class Stem(Base):
    __tablename__ = "stem"

    id        = db.Column(db.Integer, primary_key=True)
    FormType  = db.Column(db.String(5), nullable=False)
    tbl       = db.Column(db.String(64), nullable=False)
    field     = db.Column(db.String(64), nullable=False)
    version   = db.Column(db.String(20), nullable=False)
    path      = db.Column(db.String(1000), nullable=False) # Relative to group root 
    description = db.Column(db.String(1000))

class Filing(Base):
    __tablename__ = "filing"
    
    id               = db.Column(db.Integer, primary_key=True)
    EIN              = db.Column(m.CHAR(9))
    DLN              = db.Column(m.CHAR(14))
    ObjectId         = db.Column(m.CHAR(18))
    FormType         = db.Column(db.String(20))
    URL              = db.Column(db.String(100))
    OrganizationName = db.Column(db.String(120))
    SubmittedOn      = db.Column(db.Date)
    LastUpdated      = db.Column(db.DateTime)
    TaxPeriod        = db.Column(db.Date)
    IsElectronic     = db.Column(m.BIT)
    IsAvailable      = db.Column(m.BIT)

    raw = relationship("RawXML", back_populates="filing")

class RawXML(Base):
    __tablename__ = "xml"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id', ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    XML = db.Column(m.LONGTEXT)
    Version = db.Column(db.String(20))
    FormType = db.Column(db.String(5))

    filing = relationship("Filing", back_populates="raw")

    def __init__(self, xmlStr, filing, version = None, formType = None):
        self.filing = filing
        self.XML    = xmlStr
        self.Version = version
        self.FormType = formType


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

    def validateFormYr(self, y):
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
        self.FormYr      = self.validateFormYr(formYr)

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

class PartIV(Base):
    __tablename__ = "part_iv"
    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    CurExcess = db.Column(db.Boolean)
    PrevExcess = db.Column(db.Boolean)
    HasLoan = db.Column(db.Boolean)
    RelPersGrant = db.Column(db.Boolean)
    BusOrgMem = db.Column(db.Boolean)
    BusFamMem = db.Column(db.Boolean)
    BusOfficer = db.Column(db.Boolean)

    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing       = filing
        self.CurExcess    = lookup.findTrueFalse("part_iv", "CurExcess")
        self.PrevExcess   = lookup.findTrueFalse("part_iv", "PrevExcess")
        self.HasLoan      = lookup.findTrueFalse("part_iv", "HasLoan")
        self.RelPersGrant = lookup.findTrueFalse("part_iv", "RelPersGrant")
        self.BusOrgMem    = lookup.findTrueFalse("part_iv", "BusOrgMem")
        self.BusFamMem    = lookup.findTrueFalse("part_iv", "BusFamMem")
        self.BusOfficer   = lookup.findTrueFalse("part_iv", "BusOfficer")

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

class PartXII(Base):
    __tablename__ = "part_xii"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id'))
    FSAudited = db.Column(db.Boolean)
    AuditCmt = db.Column(db.Boolean)
    filing = relationship(Filing)

    def __init__(self, lookup, filing):
        self.filing    = filing
        self.FSAudited = lookup.findTrueFalse("part_xii", "FSAudited")
        self.AuditCmt  = lookup.findTrueFalse("part_xii", "AuditCmt")

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
