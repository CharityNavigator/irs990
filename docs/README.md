# Pre-generated content available!

The output of Charity Navigator's 990 second-generation decoder is available for free download at the [Open990 Community Data page](https://www.open990.com/data/). For most users, this will be easier than running the code yourself. 

Since this library was written, more and more resources have become available for analyzing the IRS e-file dataset. If you want to build your own 990 analysis tool, the author of this library has written [a how-to article on Medium](https://medium.com/@open990/the-irs-990-e-file-dataset-getting-to-the-chocolatey-center-of-data-deliciousness-90f66097a600).

## IRS Form 990 Decoder

This repository contains everything you need to get started exploring the IRS Form 990 dataset [hosted by Amazon Web Services on S3](https://aws.amazon.com/public-datasets/irs-990/). This includes instructions for an easier-to-use 990 database provided free to the public by [Charity Navigator](https://www.charitynavigator.org/).

## The `990_long` repository

As part of the [Nonprofit Open Data Collective](https://github.com/Nonprofit-Open-Data-Collective), Charity Navigator has been proud to contribute to the [eFile Master Concordance](https://github.com/Nonprofit-Open-Data-Collective/irs-efile-master-concordance-file), which provides a standardized mapping between the many XML schemas in the primary dataset. **The concordance is still in draft.** A [validation event](https://docs.google.com/forms/d/e/1FAIpQLSeYwFO7k_HzkkHYdD9s8xFXBfuL4OrWZNmxeC6cLEA26Dk_IA/viewform) took place in November 2017.

The Charity Navigator 990 Decoder and the community concordance has been the basis for several 990-related projects, including [IRSx](https://github.com/jsfenfen/990-xml-reader) and [Open990](https://www.open990.com/), as well as a body of documentation hosted by the [Nonprofit Open Data Collective](https://github.com/Nonprofit-Open-Data-Collective).

As a result of this hard work, Charity Navigator now has code capable of extracting **all fields** from the **entire** IRS eFile dataset. The data will be made publcily available after the Validatathon event. If you wish to preview the data, please follow the instructions in the readme for the [new code](https://github.com/CharityNavigator/990_long).

## Working with the original 990 Toolkit

Due to the imminent release of a much richer dataset, we have deprecated our original toolkit. If you wish to access it anyway, you can view the original documentation [here](https://charitynavigator.github.io/irs990/original).

## Authors (original version)

Code and visualizations: [David Bruce Borenstein](https://www.github.com/borenstein)

Documentation: David Bruce Borenstein and Zach Weinsteiger

Crosswalk between XML and database columns (990): Vince Bogucki

Crosswalk between XML and database columns (EZ): David Bruce Borenstein and Zach Weinsteiger
