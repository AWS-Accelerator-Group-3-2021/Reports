var currentAuthToken = location.pathname.split('/')
currentAuthToken = currentAuthToken[2]
var url = `http://localhost:8000/session/${currentAuthToken}/list/meta/reports`
console.log(url)
axios.get(url)
    .then(function (response) {
        // handle success, reports given in json format
        console.log(typeof {})
        console.log(response.data)
        console.log(Object.keys(response.data).length === 0)
        if (Object.keys(response.data).length === 0) {
            console.log('i have run')
            const para = document.createElement("p");
            para.innerHTML = "No reports found.";
            const element = document.getElementById("reportsList");
            element.appendChild(para);
        } else {
            response.data.forEach((report) => {
                
            })
        }
    })
    .catch(function (error) {
        // handle error
        document.write('There was an error in fetching the reports. Error: ' + error)
        console.log(error);
    })