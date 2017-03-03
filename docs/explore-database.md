# Exploring the 990 dataset

## Understanding (and finding) the IRS schemas

The 990 database is built from XML files supplied from the IRS. These filings are based on schemas supplied in `.xsd` format, which is a special form of XML used for describing other XML documents. Some have found these `.xsd` schemas to be hard to use.  

You can find schemas from TY 2013 through TY 2016 [on the IRS website](https://www.irs.gov/charities-non-profits/current-valid-xml-schemas-and-business-rules-for-exempt-organizations-modernized-e-file). However, the AWS data runs as far back as 2011. You can find some of the missing schemas if you look [at the directory where the listed files are located](https://www.irs.gov/pub/irs-schema/). As these are not actually listed on the index page provided by the IRS, you should exercise caution in interpreting these schemas.

There are multiple versions of the schema for each year. Within each version, there are several `.xsd` files that must be consulted in order to build the database. Field descriptions may be contained either in XML comments or in an `<xsd:documentation>` tag. If you wish to work directly with the data, be sure to look at everything, including comments.

The following files were used to build the database supplied in this toolkit.

* `TEGE/Common/ReturnHeader990x.xsd` -- metadata for filing
* `TEGE/TEGE990/ReturnData990.xsd` -- index of the files required for the filing body
* `TEGE/TEGE990/IRS990/IRS990.xsd` -- detailed descriptions of 990 fields.
* `TEGE/Common/IRS990ScheduleG/IRS990ScheduleG.xsd` -- detailed descriptions of fields on Schedule G.
* `TEGE/Common/IRS990ScheduleL/IRS990ScheduleL.xsd` -- detailed descriptions of fields on Schedule L.

## Database tables

### `filing`

The table `filing` is built from the index files directly from the IRS. It corresponds one-to-one to the records in the index. This includes non-digital filings and other filings not available on AWS. From the [AWS front matter](https://aws.amazon.com/public-datasets/irs-990/):

> Index listings of available filings are available in JSON and CSV files, organized based on the year they were filed. Index files exist for each year going back to 2011 and are named based on their year and file type. For example, the CSV index for 2011 is available at https://s3.amazonaws.com/irs-form-990/index_2011.csv, and the JSON index file for 2015 is available at https://s3.amazonaws.com/irs-form-990/index_2011.json
> 
> These index files includes basic information about each filing, including the name of the filer, the Employer Identification Number (EIN) of the filer, the date of the filing, and unique identifier for the filing.

* `id` An internal, table-specific identifier. Corresponds to `FilingId` foreign key for all other tables. This number is totally arbitrary!
* `EIN` The employer tax identification number for the organization whose filing it is.
* `DLN` The document locator number from the IRS.
* `ObjectID` This appears to be the unique part of the URL for the XML file containing the tax record. In earlier data releases from the IRS, only some records have this field. In this release, however, all filings appear to have an `ObjectID`.
* `FormType` Whether the filing is 990, 990EZ, or 990PF. 
* `URL` The URL for the XML file containing the tax record.  In earlier data releases from the IRS, only some records have this field. In this release, however, all filings appear to have a `URL`.
* `OrganizationName` The name of the organization that filed the 990.
* `SubmittedOn` The date the filing was submitted.
* `LastUpdated` It is not clear whether this refers to the date the organization last updated its filing, or the date the IRS last updated its record (or something else).
* `TaxPeriod` [**Known issue**](https://github.com/CharityNavigator/irs990/issues/6) This should show the date that the tax period ends. It currently shows the correct month and year, but provides the first day of the month instead of the last.
* `IsElectronic` In previous data releases from the IRS, this flag was used to indicate that the row corresponded to an e-filing. In the current version, all paper filings have been removed from the index, and `IsElectronic` is no longer supplied.

### Header

Several of the fields here are redundant with those in `filing`. That's because the `filing` version is pulled from the index, whereas the `header` version is pulled from the 990. Therefore, it is a reasonable sanity check to compare the two.

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `FilerEIN` -- EIN (tax ID) for 
* `TaxYr` -- Tax Year
* `Amended` -- Indicates this return is an amended return
* `FilerName1` -- Name of business
* `FilerName2` -- Name of business, 2nd line
* `PdBeginDt` -- Tax period begin date
* `PdEndDt` -- Tax period end date
* `Org501c3` -- Is it a 501(c)(3) Organization?
* `Org501cInd` -- Is it a 501(c) Organization?
* `Org501cType` -- If so, what type?
* `Org4947a1` --  Is it a 4947(a)(1) Organization?
* `Org527Ind` -- Is it a 527 Organization?
* `FormYr` -- Year of formation

### Part I

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `VoteBodyCount` -- Number Voting Members Governing Body.
* `Revenue` -- Total Revenue - Current Year.
* `Expenses`-- Total Expenses - Current Year.
* `RevLessExp` -- Revenues Less Expenses - Current Year.

### Part III

The 990 schem adocumentation for this is pretty sparse. All it says is "Repeating Activities Lines 4b through 4d." The one-word definitions below are also from the schema.

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `Description` -- Description of individual program.
* `ExpenseAmt` -- Expenses of individual program.
* `GrantAmt` -- Amount of grants included in program expenses.
* `RevenueAmt` -- Revenue generated from program.

### Part IV

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `CurExcess` -- Did the organization engage in an excess benefit transaction with a disqualified person during the year?
* `PrevExcess` -- Is the organization aware that it engaged in an excess benefit transaction with a disqualified person in the prior year?
* `HasLoan` -- Did the organization engage in loans to or from any current or former officer, director, trustee, key employee, or disqualified persons?
* `RelPersRevenue` -- Did the organization provide grants to a related person?
* `BusOrgMem` -- Was the organization a party to a business transaction with an officer, director, trustee, or key employee?
* `BusFamMem` -- Was the organization a party to a business transaction with a family member of an officer, director, trustee, or key employee?
* `BusOfficer` -- Was the organization a party to a business transaction with an organization related to an officer, director, trustee, or key employee? 

### Part VI

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `Diversion` -- Was the organization aware of a significant diversion of the organization's assets during the year?
* `HasMinutes` -- Does the organization keep meeting minutes of governing body?
* `PrvForm990` -- Does the organization provide a complete copy of the Form 990 to the governing body before filing?
* `COIPolicy` -- Does the organization have a written conflict of interest policy?
* `WBPolicy` -- Does the organization have a written whistleblower policy?
* `DocRetPolicy` -- Does the organization have a written document retention and destruction policy?
* `CeoCompProc` -- Does the organization have a CEO compensation policy based on a review and approval by an independant party?

### Part VII(a).

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `PersonNm` -- Name of individual.
* `TitleTxt` -- Title of individual.
* `AvgHrs` -- Average hours worked for the organization per week.
* `AvgHrsRltd` -- Average hours worked for related organizations per week.
* `TrustOrDir` -- Is the individual an individual trustee or director?
* `Officer` -- Is the individual an officer?
* `KeyEmpl` -- Is the individual a key employee?
* `HighComp` -- Is the individual a highest compensated employee?
* `FmrOfficer` -- Is the individual a former officer or director?
* `RptCmpOrg` -- Reportable compensation from organization.
* `RptCmpRltd` -- Reportable compensation from related organizations.
* `OtherComp` -- Other compensation.

### Part VIII

Contributions, gifts, grants and other similar amounts

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `FedCmpsAmt` -- Contributions generated through federated campaigns.
* `MemDuesAmt` -- Contributions generated through membership dues.
* `FundrAmt` -- Contributions generated through fundraising events.
* `RelOrgAmt` -- Contributions generated through related organizations.
* `GovGrntAmt` -- Contributions recieved through grants from the government.
* `OtherCntAmt` -- All other contributions, gifts, grants, and similar amounts not included in above.
* `NoncashAmt` -- Amount of contributions listed above in the form of non-cash items.
* `TtlCntAmt` -- Total amount of contributions.
* `TtlPrgRevAmt` -- Total income generated through program service revenue.
* `CntRptFndAmt` -- Contributions generated through fundraising events.
* `FndGrossAmt` -- Gross income of fundraising events.
* `FndDirExpAmt` -- Direct expenses of fundraising events.
* `TtlFndRvAmt` -- Net income of fundraising events.
* `TtlRevAmt` -- Total revenue.

### Part IX

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `GrnDomOrgAmt` -- Grants made to governments and organizations in the U.S.
* `GrnDomIndAmt` -- Grants and other assistance made to individuals in the U.S.
* `GrnFrnAmt` -- Grants and other assistance made to governments, organizations and individuals outside the U.S.
* `FundrFeesAmt`-- Total amount paid to professional fundraising services outside of the organization.
* `AffilPmtAmt`-- Total amount paid to affiliated organizations.
* `FncExpTtlAmt`-- Total amount of functional expenses.
* `FncExpSvcAmt`-- Total amount of program expenses.
* `FncExpMgtAmt`-- Total amount of administrative expenses.
* `FncExpFndAmt`-- Total amount of fundraising expenses.
* `JntCstTtlAmt`-- Total amount of joint costs.
* `JntCstSvcAmt`-- Total amount of joint costs allocated to program expenses.
* `JntCstMgtAmt`-- Total amount of joint costs allocated to administrative expenses. 
* `JntCstFdrAmt`-- Total amount of joint costs allocated to fundraising expenses.

### Part X

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `TtlRevEOYAmt`-- Total assets at fiscal year end.
* `TtlLblEOYAmt`-- Total liabilities at fiscal year end.
* `UnrAssEOYAmt`-- Total amount of unrestricted assets at fiscal year end.
* `TmpRstAssEOYAmt`-- Total amount of temporarily restricted assets at fiscal year end.
* `PrmRstAssEOYAmt`-- Total amount of permanently restricted assets at fiscal year end.
* `CapStkTrEOY`-- Capital stock or trust principle, or current funds at fiscal year end.
* `PtInCapEOYAmt`-- Paid-in or capital surplus, or land, building or equipment fund at fiscal year end.
* `RtnEndEOYAmt`-- Retained earnings, endowment, accumulated income, or other funds at fiscal year end. 
* `TtlNetEOYAmt`-- Total net assets or fund balance at fiscal year end. 
* `SFAS117Yes`-- The organization follows SFAS 117 (ASC 958). 
* `SFAS117No`-- The organization does not follow SFAS 117 (ASC 958).

### Part XII

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `FSAudited`-- Were the organization's financial statements compliled or reviewed by an independant accountant?
* `AuditCmt`-- Does the organization have an audit oversight committee?

### Schedule G

* `id` -- arbitrary, table-specific ID number.
* `FilingId` -- foreign key of `filing` table; corresponds to `filing.id`. 
* `PersonNm` -- Name of individual
* `BusinessNm1` -- Name of entity (fundraiser), line 1.
* `BusinessNm2` -- Name of entity (fundraiser), line 2.
* `ActivityTxt` -- Description of activity.
* `FndControl` -- Did fundraiser have custody or control of contributions?
* `GrsRcptAmt` -- Gross receipts from activity.
* `ContractAmt` -- Amount paid to (or retained by) fundraiser.
* `OrgNetAmt` -- Amount paid to (or retained by) organization.

### Schedule L, Part II

**NOTE: There is currently an open [issue](https://github.com/CharityNavigator/irs990/issues/5) with our processing of Schedule L. Please do not use it.**

## Data quality issues

### Issues specific to this dataset

For known issues related to this dataset, see our [issues page](https://github.com/CharityNavigator/irs990/issues).

### Upstream issues

#### Multiple 990s for the same EIN

#### Institutional trustees vs board members
  
