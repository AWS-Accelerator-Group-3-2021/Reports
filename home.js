function checkPassword() {
  const origin = location.origin
  var pwd = document.getElementById("authkeyfield").value;

  var checkURL = `${origin}/passwordCheck`

  axios({
    method: 'post',
    url: checkURL,
    data: {
      "data": pwd
    },
    headers: {
      'ReportsAccessCode': 'AWSGroup3-POCwej69',
      "Content-Type": 'application/json'
    }
  }).then((response) => {
    if (response.data.startsWith("Authorisation successful!")) {
      document.getElementsByClassName('updateLabel')[0].style.visibility = "visible"
      console.log('Auth successful.')
      var tempAuthToken = response.data.substring(43)
      console.log(tempAuthToken)
      setTimeout(() => {
        document.location = `${origin}/session/` + tempAuthToken + '/list'
      }, 2000)
    } else {
      document.getElementsByClassName('updateLabel')[0].style.visibility = "hidden"
      alert("Incorrect password. Please try again!")
      console.log('Auth unsuccessful')
    }
  })
}