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

Here is an example of the perfect datetime string: `2021-12-20T8:08:26 GMT`

If the datetime is not in GMT, does not follow the format shown above or isn't in a string data type, your request may be rejected or the reports' datetime will be incorrectly represented.

## Authorisation
The Reports System takes security seriously and rejects anything that it does not deem to be secure or have the right credentials.

### User Authentication
Every user who is authorised to use the system by the system admin and has a password to log-in to the system goes to the main homepage of the system, enters their password and logs in.
Behind the scenes, with the entered password, a `passwordCheck` POST `http` request is made containing the entered password.

> Learn more about HTTP POST requests [here](https://en.wikipedia.org/wiki/POST_(HTTP))

If the password is valid, the server will respond with a successful message of `Authorisation successful! Temp auth token: <AUTH TOKEN HERE>` where `<AUTH TOKEN HERE>` will be replaced by a randomly generated temporary auth token that the user can use to authenticate and access the server's resources.
> More about auth tokens [here](#auth-tokens)

If not, the system will respond with an error message (still with a response status code of `200` however) saying `Authorisation failed!`. In this event, it is recommended to show an error message to the user and tell them to re-enter their password.

The post request should be made to `${origin}/passwordCheck` where `${origin}` is the home URL of where the server is hosted.

#### Password Check Headers
The request must also have two headers, namely `Content-Type` and `ReportsAccessCode` in a [JSON](https://wikipedia.com/wiki/JSON) format as such:

```json
{
  "Content-Type": "application/json",
  "ReportsAccessCode": "<SERVER ACCESS CODE HERE>"
}
```

> To learn about what the `ReportsAccessCode` is, see [here](#reports-access-code)

#### Password Check Body
The `passwordCheck` POST request body should be in JSON format, as also shown above via `Content-Type` being `application/json`.

Here is an example of a perfect `passwordCheck` request body:
```json
{
  "data": "<PASSWORD HERE>"
}
```
where `<PASSWORD HERE>` is to be replaced with the password given by the user.

#### Auth Tokens
Every time a successful `passwordCheck` request is made, a randomly generated 10 character long authentication token is generated which can be used to log into authenticated `session`s. A `session` is defined as any time a user is on a webpage that requires user authentication.

For example, to see the list of reports in the system, a user would have to go to `${origin}/session/<AUTH TOKEN>/list` to access it. All other webpages, such as `Report Details` (which is `${origin}/session/<AUTH TOKEN>/list/report/<REPORT ID>` where `<REPORT ID>` is the unique ID of the report) would require a valid and active authenticated token in the URL.

With the auth token received from the response from the `passwordCheck` request, your application can create any authenticated session by simply adding the auth token at the end of `${origin}/session/` and, if valid, they would be able to access secured information. Auth tokens only last 24 hours so you will have to generate a new auth token by making a `passwordCheck` request once again.

If your auth token has expired and you try to access any webpage using an authenticated `session`, you will likely receive an error HTML response saying that your auth token is invalid and will tell you to make a new auth token by making a `passwordCheck` request.

For example, a visit to `${origin}/session/abc123/list/report/test1` with the invalid auth token of `abc123` will have a response of `<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>`.

### Client Authentication
[User Authentication](#user-authentication) and [Client Authentication](#client-authentication) differ in the sense that Client Authentication is used by applications in mostly [CRUD Operations](#crud-operations).

In fact, Client Authentication is actually a part of User Authentication, because User Authentication requires a `passwordCheck` POST request with headers consisting of `Content-Type` and `ReportsAccessCode` (more information [here](#reports-access-code)), both of which are required for all POST requests to The Reports System.

Since Client Authentication is best explained with an example, consider this; if you have an application and would like to make a `newReport` using the [`newReport` endpoint](#new-report), in order for The Reports System to identify that you are a verified application trying to make a change in the reports, you will have to include those two headers of `Content-Type` and `ReportsAccessCode` in your POST request.

#### Reports Access Code
All POST requests to The Reports System require two headers of `Content-Type` and `ReportsAccessCode` (in part mentioned in [here](#client-authentication)) in JSON format as such:
```json
{
  "Content-Type": "application/json",
  "ReportsAccessCode": "<REPORTS ACCESS CODE HERE>"
}
```

A `ReportsAccessCode` is a form of authentication that The Reports System accepts to ensure that you are a verified client accessing the system. This code can only be gotten by the system admin. If this code is wrong, you are likely to receive an error response as such (still with a status code of `200` however): `Authorisation failed! Incorrect reports access code or content-type.`. In this event, you will have to manually update your code with the correct access code.

## CRUD Operations
The Reports System has several endpoints related to performing operations on reports, namely [`newReport`](#new-report), [`updateReport`](#update-report), and [`deleteReport`](#delete-report). These endpoints make up 3 out of the 4 CRUD Operations most storage systems have. Don't know what CRUD is? Refer [here](https://wikipedia.com/wiki/CRUD)

### New Report
In order to make a new report, a client has to make a POST request that conform to [client authentication requirements](#client-authentication) and the body of the request must follow the [report model](#report-model).

Here is an example of the perfect new report POST `http` request:

URL: `${origin}/newReport`
Headers:
```json
{
  "Content-Type": "application/json",
  "ReportsAccessCode": "<REPORTS ACCESS CODE HERE>"
}
```
Body:
```json
{
  "data": {
    "id": "454732AF-6B1C-42AC-A274-9B93CA853994",
    "reporter_name": "Prakhar Trivedi",
    "add_info": "One morning, I just felt bad, and thought of reporting some people in the neighbourhood.",
    "measurement": "2.0m",
    "address": "Block 69C, Bedok Street 89, Bedok, Singapore, 278544",
    "datetime": "2021-12-20T08:22:48 GMT",
    "clientInfo": "iPhone 13 Pro Max, iOS 15.2"
  }
}
```

If any one of the parameters are missed in the [report model](#report-model), the request will be rejected and a response like this will be received: `Invalid report data. Missing key: <MISSING KEY>` where `<MISSING KEY>` is the name of the missing parameter, for e.g `address`.

If both headers are not present or have incorrect values, the following responses will be received respectively: `ReportsAccessCode header or Content-Type header was not present in request. Request rejected.` and `Authorisation failed! Incorrect reports access code or content-type.`.

If the ID of the report is already present (which should not be the case since its a UUID, ensure you are not intending to actually use the `updateReport` endpoint), a response such as this will be received: `Report already exists! Please use the update report endpoint to update the report.`.

### Update Report
In order to update a report, a client can use the `updateReport` endpoint to update a report with a given report ID. The `http` POST request should be sent to `${origin}/updateReport` and should conform to [client authentication requirements](#client-authentication) and also the report must be formatted according to the [Report model](#report-model). In the POST request, the client sends an updated Report with some different parameter values. Upon receiveing the request, The Reports System replaces its current save of the report with the report sent in the request by finding it using the ID given. (The report ID cannot be changed.)

Here is an example of the perfect http POST request to `updateReport`:

URL: `${origin}/updateReport`

Headers:
```json
{
  "Content-Type": "application/json",
  "ReportsAccessCode": "<REPORTS ACCESS CODE>"
}
```

Body:
```json
{
  "data": {
    "id": "454732AF-6B1C-42AC-A274-9B93CA853994",
    "reporter_name": "Prakhar Trivedi",
    "add_info": "One morning, I just felt bad, and thought of reporting some people in the neighbourhood.",
    "measurement": "2.2m", // this parameter is updated
    "address": "Block 69C, Bedok Street 89, Bedok, Singapore, 278544",
    "datetime": "2021-12-20T08:22:48 GMT",
    "clientInfo": "iPhone 13 Pro Max, iOS 15.2"
  }
}
```

If any one of the parameters are missed in the [report model](#report-model), the request will be rejected and a response like this will be received: `Invalid report data. Missing key: <MISSING KEY>` where `<MISSING KEY>` is the name of the missing parameter, for e.g `address`.

If both headers are not present or have incorrect values, the following responses will be received respectively: `ReportsAccessCode header or Content-Type header was not present in request. Request rejected.` and `Authorisation failed! Incorrect reports access code or content-type.`.

If the report ID given in the request does not exist in the server's records, the request will be rejected and you will receive a response like `No such report exists in server. To make a new report, please use the new report endpoint.`.

### Delete Report
This one is rather quite simple. The client can send a `http` POST request to a `deleteReport` endpoint to delete a report with a given ID and The Reports System will permanently delete the report. The request should conform to [client authentication requirements](#client-authentication) and only requires to report ID to delete in the body.

Here is an example of a perfect http POST request to `deleteReport`:

URL: `${origin}/deleteReport`

Headers:
```json
{
  "Content-Type": "application/json",
  "ReportsAccessCode": "<REPORTS ACCESS CODE HERE>"
}
```

Body:
```json
{
  "data": {
    "id": "454732AF-6B1C-42AC-A274-9B93CA853994"
  }
}
```

If both headers are not present or have incorrect values, the following responses will be received respectively: `ReportsAccessCode header or Content-Type header was not present in request. Request rejected.` and `Authorisation failed! Incorrect reports access code or content-type.`.

If no report ID is provided in the request body, an error response (still with a status code of `200` however) of `Invalid request. No report ID was provided.` will be obtained.

If The Reports System finds no report with the report ID given in the request, an error response (still with a status code of `200` however) of `No such report exists in server. To make a new report, please use the new report endpoint.`

### Report Meta Data
The Reports System consists of two ways that a client can get report data in raw format. Due to the design of the system, there are two sites where a [GET `http` request](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) will allow a client to get report information.

Before attempting to get any information at all, the client will have to get an [auth token](#auth-tokens) using a [`passwordCheck` POST request](#user-authentication).

**If you know the ID of the report you are intending to get information of, skip the section and go to [Accessing Individual Report Data](#accessing-individual-report-data)**

#### Getting Report IDs
There is a high change your client does not have the IDs of the reports to access them, hence, the client will have to send a GET request to `${origin}/session/<AUTH TOKEN HERE>/list/meta/reportIDs`.

This request does not need to have any headers or body as the authentication is done via the auth token itself. Do note that if the auth token is invalid you will get a HTML error response (still with a status code of `200` however) `<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>`.

A successful request will get an array of report IDs with each element having a string data type as a response.

Here is an example request and response pair:

**Request**

URL: `${origin}/session/exampleAuthToken/list/meta/reportIDs`

**Response**

```
['report1', 'report2', 'report3']
```

#### Accessing Individual Report Data
With an auth token and report ID, you can then directly get all raw JSON data of a report by making a GET request to `${origin}/session/<AUTH TOKEN HERE>/list/meta/report/<REPORT ID HERE>`.

This request does not need to have any headers or body as the authentication is done via the auth token itself. Do note that if the auth token is invalid you will get a HTML error response (still with a status code of `200` however) `<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>`.

The response will be in JSON format and will have all of the parameters in the [report model](#report-model) except for the ID (well, because the client already have it).

Here is an example request and response pair:

**Request**

URL: `${origin}/session/sampleAuthToken/list/meta/report/report2`

**Response (This is pretty-printed)**

```json
{
   "reporter_name": "Prakhar Trivedi",
   "add_info": "One morning, I just felt bad, and thought of reporting some people in the neighbourhood.",
   "measurement": "2.0m",
   "address": "Block 69C, Bedok Street 89, Bedok, Singapore, 278544",
   "datetime": "2021-12-20T08:22:48 GMT",
   "clientInfo": "iPhone 13 Pro Max, iOS 15.2"
}
```

## Miscellaneous Endpoints

## URL Map
