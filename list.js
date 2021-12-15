var currentAuthToken = location.pathname.split('/')
currentAuthToken = currentAuthToken[2]
var url = `http://localhost:8000/session/${currentAuthToken}/list/meta/reportIDs`
console.log(url)
axios.get(url)
    .then(function (response) {
        // handle success
        // Object.keys(response.data).length === 0
        console.log(response.data)
        // Check if fetched meta report IDs is existent
        if (response.data.length == 0) {
            const para = document.createElement("p");
            para.innerHTML = "No reports found.";
            const element = document.getElementById("reportsList");
            element.appendChild(para);
        } else {
            // With given report ID, fetch the report meta data
            response.data.forEach(reportID => {
                const metaReportURL = `http://localhost:8000/session/${currentAuthToken}/list/meta/report/${reportID}`
                axios.get(metaReportURL)
                    .then(response => {
                        if (response.statusText == 'OK') {
                            if (response.data != '<h1>Report not found. Please check the report ID and try again.</h1>') {
                                // Report meta data successfully received
                                // Make para elem with report meta data
                                const para = document.createElement("p");
                                const hrefElem = document.createElement("A");
                                hrefElem.href = ""
                                hrefElem.target = "_blank"
                                hrefElem.innerHTML = textFileName

                                para.appendChild(hrefElem);

                                const element = document.getElementById("dataBankFilesList");
                                element.appendChild(para);
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