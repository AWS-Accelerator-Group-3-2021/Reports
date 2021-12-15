var splitPath = location.pathname.split('/')
const currentAuthToken = splitPath[2]
const currentReportID = splitPath[5]
const origin = location.origin

axios.get(`${origin}/session/${currentAuthToken}/list/meta/report/${currentReportID}`)
    .then(response => {
        if (response.status == 200) {
            if (response.data != '<h1>Report not found. Please check the report ID and try again.</h1>') {
                document.getElementById('reportIDLabel').innerHTML = `Report ID: ${currentReportID}`

                document.getElementById('reportAuthorLabel').innerHTML = `Author: ${response.data.reporter_name}`
                document.getElementById('reportMeasurementLabel').innerHTML = `Measurement: ${response.data.measurement}`
                document.getElementById('reportAddressLabel').innerHTML = `Address of Report: ${response.data.address}`
                document.getElementById('reportAddInfoLabel').innerHTML = `Additional Information: ${response.data.add_info}`
                document.getElementById('reportClientInfoLabel').innerHTML = `Client Information: ${response.data.clientInfo}`
                document.getElementById('reportDatetimeLabel').innerHTML = `Date and time: ${response.data.datetime}`
            } else {
                document.write('There was an error in fetching the report details. This is likely a server error. Please try again.')
                console.log('Received incorrect report ID response with the incorrect ID being: ' + currentReportID)
            }
        } else {
            document.write('There was an error in fetching the report details. This is likely a server error. Please try again.')
            console.log('Received non-200 status code response from server.')
        }
    })
    .catch(err => {
        document.write(`There was an error in fetching the report details. Error: ${err}`)
        console.log('Error in fetching report details: ' + err)
    })