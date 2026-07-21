# AXIS Scale Database Reader

A desktop application for transforming raw AXIS Scale weighing-system data into professional waste-management reports.

## Overview

AXIS Scale exports contain operational weighing records that are often difficult to use directly for administrative and reporting purposes. This application automates the process of importing raw CSV exports, matching location identifiers to tenant information, and generating structured PDF reports ready for business use.

Originally developed to support commercial waste-reporting workflows where large volumes of weighing data needed to be consolidated, verified, and presented in a clear format for administrative staff.

## Problem

Raw AXIS Scale data contains:

- Technical identifiers instead of tenant names
- Large amounts of weighing records
- Data that requires manual processing before reporting
- No tenant-oriented waste summaries

Preparing reports manually can be time-consuming and error-prone.

This tool automates the entire workflow by:

1. Importing AXIS Scale CSV exports
2. Resolving location identifiers through a configurable tenant mapping file
3. Filtering records by reporting period
4. Aggregating waste quantities by waste code
5. Generating a professional PDF report

## Features

- Import AXIS Scale CSV exports
- Tenant mapping through configurable CSV files
- Persistent tenant-key storage
- Date-range filtering
- Waste-code aggregation
- Tenant-specific summaries
- Automatic PDF report generation
- Simple desktop GUI
- Designed for non-technical administrative users

## Reporting Output

The generated PDF includes:

### Global Summary

- Waste codes
- Total collected weight
- Aggregated waste statistics

### Tenant Breakdown

For each tenant:

- Waste code summary
- Total reported weight
- Individual waste-category breakdown

### Reporting Period

Reports can be generated for any selected date range.

## Tenant Mapping

The application supports user-friendly tenant names through a mapping file.

Example:

| Location ID | Tenant Name |
|------------|-------------|
| A101 | Store A |
| B205 | Store B |
| C311 | Store C |

The mapping file is stored locally and only needs to be updated when tenant information changes.

## Workflow

1. Load the tenant mapping CSV.
2. Load the AXIS Scale export CSV.
3. Select the reporting period.
4. Generate the report.
5. Save the generated PDF.

## Use Case

This software was originally developed to support waste-management reporting in a commercial environment where weighing-system exports required regular processing for operational and administrative reporting.

## Technologies

- Python
- Pandas
- Tkinter
- ReportLab

## License

MIT
