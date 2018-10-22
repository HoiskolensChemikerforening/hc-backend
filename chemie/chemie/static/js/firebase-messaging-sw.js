importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-messaging.js');
firebase.initializeApp({
    messagingSenderId: "1057998917777"
});
messaging.onMessage(function(payload){
    // When user is present on the site, they are instead presented with a toast message.
    var snackbar = document.getElementById("snackbar");
    snackbar.innerHTML = payload.notification.body
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);
  });

