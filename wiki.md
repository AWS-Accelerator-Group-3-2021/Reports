# The Reports System Wiki

This wiki contains all information regarding accessing The Reports System (or just Reports server) via its various endpoints 
that deal with the handling, storing, updating and creation of Reports.

## Table Of Contents:
- [Models](#models)
- [Authorisation](#authorisation)
- [CRUD Operations](#crud-operations)
- [Miscellaneous Endpoints](#miscellaneous-endpoints)

## Models
The Reports System has a couple of models (i.e structure of data) that it works with when handling report information.

### Report Model
Every report that goes in or out of the reports system has to follow the `Report` model, which is a format consisting of several parameters that withhold report information.

Parameters:
- `id`: This parameter must be unique for every report, and hence must be a newly generated UUID string, preferrably with a UUID5 engine. For more information on what a UUID is, refer [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)
- `reporter_name`: This parameter should have a string data type and is pretty self-explanatory; it should contain the name of the person making this report.
- `add_info`: The shorthand in this parameter stands for `Additional Information`, which should contain more information about the report, for e.g why the person reporting made this report. This information is to be obtained by asking the user. This parameter should also have a string data type.
- `measurement`: This parameter should have a string data type and should follow this format: `<Decimal number of measurement in metres>m`, for e.g `1.4m`. This is the measurement of the report that is being made.
- `address`: This parameter should have a string data type and should contain the address of the offendee in question of the report.
- `clientInfo`: This parameter should have a string data type and should contain information about from which platform is this report being made and sent, for e.g `iPhone 13 Pro Max, iOS 15.2`. As a general rule, this parameter should at least have the model of the phone and the current OS its running if the report is being made from a mobile app.
- `datetime`: This parameter should have a string data type and should follow the [Datetime model](#datetime-model)

All of the above parameters are compulsory to have in any form of API request that takes in a Report model formatted report, otherwise the request will be rejected.

### Datetime Model
The datetime model describes how The Reports System accepts the date and time of a report.

Every datetime string should be formatted in this format: `yyyy-MM-dd'T'HH:mm:ss z` (This is the exact format most languages' date formatters use.)

In the format, the `T` in the middle should be joining the date and time and the `z` at the end represents the timezone which must always be in GMT. Any date should be first converted to the GMT timezone and then converted to a string in the format shown below. 

If the datetime is not in GMT, does not follow the format shown above or isn't in a string data type, your request may be rejected or the reports' datetime will be incorrectly represented.

## Authorisation


## CRUD Operations

## Miscellaneous Endpoints
