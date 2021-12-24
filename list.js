var currentAuthToken = location.pathname.split('/')
currentAuthToken = currentAuthToken[2]
var origin = location.origin
var url = `${origin}/session/${currentAuthToken}/list/meta/reportIDs`

//Date compairson function
function compare(a, b) {
    const aDate = new Date(a.datetimeWithoutGMTText)
    const bDate = new Date(b.datetimeWithoutGMTText)
    if (aDate > bDate) {
        return -1
    }
    if (aDate < bDate) {
        return 1
    }
    return 0;
}

function renderReport(report) {
    // console.log("reached here")
    const para = document.createElement("p");
    const hrefElem = document.createElement("A");
    hrefElem.href = `${origin}/session/${currentAuthToken}/list/report/${report.id}`
    hrefElem.target = "_blank"
    hrefElem.innerHTML = `Measurement: ${report.measurement}, By: ${report.reporter_name}, ID: ${report.id}`

    // Add delete report button to para element
    const deleteButton = document.createElement("button")
    deleteButton.innerHTML = "Delete"
    deleteButton.onclick = function () {
        alert(`Are you sure you want to delete report ${report.id}?`)
        var url = `${origin}/deleteReport`
        var data = {
            "data": {
                "id": report.id
            }
        }
        var headers = {
            "Content-Type": "application/json",
            "ReportsAccessCode": "AWSGroup3-POCwej69"
        }
        axios({
            method: 'post',
            url: url,
            data: data,
            headers: headers
        })
        .then(response => {
            if (response.status == 200) {
                if (response.data == "Report deleted successfully!") {
                    if (!alert("Report deleted successfully!")) {
                        window.location.reload()
                    }
                } else {
                    if (response.data == "No such report exists in server. To make a new report, please use the new report endpoint.") {
                        alert("Failed to delete report as no such report was found in server.")
                        console.log(response.data)
                    } else {
                        alert(response.data)
                        console.log(response.data)
                    }
                }
            } else {
                alert("Error in connecting to The Reports System. Please try again.")
                console.log("Non-200 status code returned from deleteReport endpoint.")
            }
        })
        .catch(err => {
            console.log("Error in deleteing report: " + err)
            alert("There was an error in deleteing the report: " + err)
        })
    }
    deleteButton.className = "deleteButtons"
    // Add spacing to deleteButton on the left
    const deleteSpacing = document.createElement("span")
    deleteSpacing.innerHTML = "&nbsp;&nbsp;&nbsp;&nbsp;"

    para.appendChild(hrefElem);
    para.appendChild(deleteSpacing)
    para.appendChild(deleteButton);

    const element = document.getElementById("reportsList");
    element.appendChild(para);
}

// Actual fetching of IDs and reports
axios.get(url)
    .then(function (idsArray) {
        // handle success
        // Check if fetched meta report IDs is existent
        if (idsArray.data.length == 0) {
            const para = document.createElement("p");
            para.innerHTML = "No reports found.";
            const element = document.getElementById("reportsList");
            element.appendChild(para);
        } else {
            // With given report ID, fetch the report meta data
            var reports = []
            idsArray.data.forEach(reportID => {
                const metaReportURL = `${origin}/session/${currentAuthToken}/list/meta/report/${reportID}`
                axios.get(metaReportURL)
                    .then(metaDataResponse => {
                        if (metaDataResponse.status == 200) {
                            if (metaDataResponse.data != '<h1>Report not found. Please check the report ID and try again.</h1>') {
                                // Report meta data successfully received
                                // Make para elem with report meta data
                                const datetimeWithoutGMTText = metaDataResponse.data.datetime.split(" ")[0]

                                var newData = metaDataResponse.data
                                newData.datetimeWithoutGMTText = datetimeWithoutGMTText
                                newData.id = reportID

                                reports.push(newData)
                                reports.sort(compare)
                                document.getElementById('reportsList').innerHTML = ""
                                reports.forEach(report => {
                                    renderReport(report)
                                })
                            } else {
                                // invalid/non-existent report ID
                                document.write('There was an error in fetching a report correctly due to an incorrect report ID being received. This is likely a server error. Please try again.')
                                console.log("Failed to get report with incorrect ID: " + reportID)
                            }
                        } else {
                            // Request failed, likely due to server error
                            document.write('There was an error in fetching a report from the server. This is likely a server error. Please try again.')
                            console.log('Failed to fetch report with ID: ' + reportID + ' from server.')
                        }
                    })
                    .catch(err => {
                        document.write('There was an error in fetching the reports. Error: ' + error)
                        console.log(error);
                    })
            })
        }
    })
    .catch(function (error) {
        // handle error
        document.write('There was an error in fetching the reports. Error: ' + error)
        console.log(error);
    })

function gotoReport() {
    var reportID = prompt("Enter report's ID:")
    if (!reportID || reportID == "") {
        return
    }
    document.location = `${origin}/session/${currentAuthToken}/list/report/${reportID}`
}