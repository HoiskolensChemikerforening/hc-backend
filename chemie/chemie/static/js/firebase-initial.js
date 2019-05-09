// Main script which is called in base.html for logged in users
// For better understanding of firebase initial se url:
// https://firebase.google.com/docs/cloud-messaging/js/client
//----------------------------------------

// Firebase front-end configurations, these API key are suppost to be public,
var config = {
    apiKey: "AIzaSyDZ8vCkF4evPls5g708fgYnV2grx4FmJkk",
    authDomain: "chemie-da469.firebaseapp.com",
    databaseURL: "https://chemie-da469.firebaseio.com",
    projectId: "chemie-da469",
    storageBucket: "chemie-da469.appspot.com",
    messagingSenderId: "775983543184"
};
firebase.initializeApp(config);

// JS initializer a Service worker which is running in the brower while you are not present
// on hc.ntnu.no, this allowes for push notification when you are not active on site
const messaging = firebase.messaging();
navigator.serviceWorker.register('/static/js/firebase-messaging-sw.js')
    .then(function (registration) {
        messaging.useServiceWorker(registration);

        // The user is requestet for permission to recieve notifications
        if (window.location.href == "https://hc.ntnu.no/" || window.location.href == "http://127.0.0.1:8000/") { //Only prompts permission on home page or running as local host
            var browser = getBrowser();
            if (browser == "Chrome") {
                messaging.requestPermission()
                    .then(function () {
                        // The token is the device personalized ID which is auto generated
                        // every time the user accept the requested permission
                        return messaging.getToken();
                    }).then(function (token) {
                        // Saving device token backend as Device object
                        // at hc.ntnu.no server to be used when notification is to be sent

                        postAjax("web_push/save/", { 'token': token, 'browser': browser });
                    }).catch(function (err) {
                        if (!err.code == "messaging/permission-blocked") {
                            throw err;
                        }
                    });
            } else if (browser == 'Safari') {
                /*
                The commented lines below is the implementation for Safari browser
                Apples APNS certificat would be needed, cost ~1000 NOK/year
                The code has not been testet so no garanties it would work
                */

                // messaging.requestPermission()
                //     .then(function () {
                //         return messaging.getToken();
                //     }).then(function (token) {
                //         // Saving device token backend as Device object to be used when notification is to be sent
                //         postAjax("web_push/save/", { 'token': token, 'browser': browser });
                //     }).catch(function (err) {
                //         if (!err.code == "messaging/permission-blocked") {
                //             throw err;
                //         }
                //     });
            }
        }
    });

// When user is present on the site,
// they are presented with a toast message instead of the service workers push notification.
messaging.onMessage(function (payload) {
    M.toast({ html: payload.notification.body, classes: 'blue darken-3 rounded' })
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

// A post function which fetched the CSRF-token before posting
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
            console.log("Device registered");
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
