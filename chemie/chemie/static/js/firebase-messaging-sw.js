// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
    apiKey: "AIzaSyBiK7kDOZlPR_6QQyX8pxsrY3RHtlSKewQ",
    authDomain: "chemie-4a9d7.firebaseapp.com",
    databaseURL: "https://chemie-4a9d7.firebaseio.com",
    projectId: "chemie-4a9d7",
    storageBucket: "chemie-4a9d7.appspot.com",
    messagingSenderId: "949677257241"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();