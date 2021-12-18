var currentAuthToken = location.pathname.split('/')
currentAuthToken = currentAuthToken[2]
var origin = location.origin
var url = `${origin}/session/${currentAuthToken}/list/meta/reportIDs`
console.log(url)

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

// Actual fetching of IDs and reports
axios.get(url)
    .then(function (response) {
        // handle success
        // Object.keys(response.data).length === 0
        // console.log(response.data)
        // Check if fetched meta report IDs is existent
        if (response.data.length == 0) {
            const para = document.createElement("p");
            para.innerHTML = "No reports found.";
            const element = document.getElementById("reportsList");
            element.appendChild(para);
        } else {
            // With given report ID, fetch the report meta data
            var reports = []
            var loopCount = 0
            response.data.forEach(reportID => {
                const metaReportURL = `${origin}/session/${currentAuthToken}/list/meta/report/${reportID}`
                axios.get(metaReportURL)
                    .then(response2 => {
                        if (response2.status == 200) {
                            if (response2.data != '<h1>Report not found. Please check the report ID and try again.</h1>') {
                                // Report meta data successfully received
                                // Make para elem with report meta data
                                const datetimeWithoutGMTText = response2.data.datetime.split(" ")[0]

                                var newData = response2.data
                                newData.datetimeWithoutGMTText = datetimeWithoutGMTText
                                newData.id = reportID

                                reports.push(newData)
                                reports.sort(compare)
                                console.log(reports.length)
                                if (loopCount == (response.data.length)) {
                                    reports.forEach(report => {
                                        console.log("reached here")
                                        const para = document.createElement("p");
                                        const hrefElem = document.createElement("A");
                                        hrefElem.href = `${origin}/session/${currentAuthToken}/list/report/${report.id}`
                                        hrefElem.target = "_blank"
                                        hrefElem.innerHTML = `Measurement: ${report.measurement}, By: ${report.reporter_name}, ID: ${report.id}`
                                        para.appendChild(hrefElem);

                                        const element = document.getElementById("reportsList");
                                        element.appendChild(para);
                                    })
                                }
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
                loopCount += 1
            })
        }
    })
    .catch(function (error) {
        // handle error
        document.write('There was an error in fetching the reports. Error: ' + error)
        console.log(error);
    })