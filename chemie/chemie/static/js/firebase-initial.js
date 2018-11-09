// Main script
//----------------------------------------
var config = { // Firebase front-end configurations
    apiKey: "AIzaSyBiK7kDOZlPR_6QQyX8pxsrY3RHtlSKewQ",
    authDomain: "chemie-4a9d7.firebaseapp.com",
    databaseURL: "https://chemie-4a9d7.firebaseio.com",
    projectId: "chemie-4a9d7",
    storageBucket: "chemie-4a9d7.appspot.com",
    messagingSenderId: "949677257241"
};
firebase.initializeApp(config);
const messaging = firebase.messaging();
navigator.serviceWorker.register('/static/js/firebase-messaging-sw.js')
    .then(function (registration) {
        messaging.useServiceWorker(registration);
        if (window.location.href == "https://chemie.no/") { //Only prompts permission on home page
            messaging.requestPermission()
                .then(function () {
                    return messaging.getToken();
                }).then(function (token) {
                // Saving device token backend to be used when notification is to be sent
                var browser = getBrowser();
                postAjax("notifications/save/", {'token': token, 'browser': browser});
            })
        }
    })
    .catch(function (err) {
        console.log(("Error Occured:"));
    });

messaging.onMessage(function (payload) {
    console.log(payload);
    // When user is present on the site, they are presented with a toast message instead of the notification.
    var snackbar = document.getElementById("snackbar");
    snackbar.innerHTML = payload.notification.body;
    snackbar.className = "show";
    setTimeout(function () {
        snackbar.className = snackbar.className.replace("show", "");
    }, 3000);
});

// Functions
//-----------------------------------------------------------

//Gives the CSRF token to be used in a AJAX POST request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}

function postAjax(url, data) {
    var params = typeof data == 'string' ? data : Object.keys(data).map(
        function (k) {
            return encodeURIComponent(k) + '=' + encodeURIComponent(data[k])
        }
    ).join('&');

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xhr.open('POST', url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState > 3 && xhr.status == 200) {
            console.log("Device registred");
        }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    var csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(params);
    return xhr
}


function getBrowser() {
    var browser = null
    if ((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1) {
        browser = 'Opera'
    }
    else if (navigator.userAgent.indexOf("Chrome") != -1) {
        browser = 'Chrome'
    }
    else if (navigator.userAgent.indexOf("Safari") != -1) {
        browser = 'Safari'
    }
    else if (navigator.userAgent.indexOf("Firefox") != -1) {
        browser = 'Firefox'
    }
    else if ((navigator.userAgent.indexOf("MSIE") != -1) || (!!document.documentMode == true)) //IF IE > 10
    {
        browser = 'IE'
    }
    return browser
}
