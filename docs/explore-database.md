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

* `id`
* `FilingId`
* `FilerEIN`
* `TaxYr`
* `Amended`
* `FilerName1`
* `FilerName2`
* `PdBeginDt`
* `PdEndDt`
* `Org501c3`
* `Org501cInd`
* `Org501cType`
* `Org4947a1`
* `Org527Ind`
* `FormYr`

### XML (large database only)

### Part I

* `id`
* `FilingId`
* `VoteBodyCount`
* `Revenue`
* `Expenses`
* `RevLessExp`

### Part III

* `id`
* `FilingId`
* `Description`
* `ExpenseAmt`
* `GrantAmt`
* `RevenueAmt`

### Part IV

* `id`
* `FilingId`
* `CurExcess`
* `PrevExcess`
* `HasLoan`
* `RelPersGrant`
* `BusOrgMem`
* `BusFamMem`
* `BusOfficer`

### Part VI

* `id`
* `FilingId`
* `Diversion`
* `HasMinutes`
* `PrvForm990`
* `COIPolicy`
* `WBPolicy`
* `DocRetPolicy`
* `CeoCompProc`

### Part VII(a).

* `id`
* `FilingId`
* `PersonNm`
* `TitleTxt`
* `AvgHrs`
* `AvgHrsRltd`
* `TrustOrDir`
* `Officer`
* `KeyEmpl`
* `HighComp`
* `FmrOfficer`
* `RptCmpOrg`
* `RptCmpRltd`
* `OtherComp`

### Part VIII

* `id`
* `FilingId`
* `FedCmpsAmt`
* `MemDuesAmt`
* `FundrAmt`
* `RelOrgAMt`
* `GovGrntAmt`
* `OtherCntAmt`
* `NoncashAmt`
* `TtlCntAmt`
* `TtlPrgRevAmt`
* `CntRptFndAmt`
* `FndGrossAmt`
* `FndDirExpAmt`
* `TtlFndRvAmt`
* `TtlRevAmt`

### Part IX

### Part X

### Part XII

### Schedule G

### Schedule L

## Data quality issues

### Issues specific to this dataset

For known issues related to this dataset, see our [issues page](https://github.com/CharityNavigator/irs990/issues).

### Upstream issues

#### Multiple 990s for the same EIN

#### Institutional trustees vs board members
