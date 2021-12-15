const currentAuthToken = location.pathname.substring(6)
var url = `http://localhost:8000/session/${currentAuthToken}/list/meta/reports`
axios.get(url)
    .then(function (response) {
        // handle success, reports given in json format
        if (response.data == {}) {
            const para = document.createElement("p");
            para.innerHTML = "No reports found.";
            const element = document.getElementById("reportsList");
            element.appendChild(para);
        } else {
            response.forEach((report) => {
                console.log(report)
            })
        }
    })
    .catch(function (error) {
        // handle error
        document.write('There was an error in fetching the reports. Error: ' + error)
        console.log(error);
    })