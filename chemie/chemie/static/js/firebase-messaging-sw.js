// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
    apiKey: "AIzaSyDZ8vCkF4evPls5g708fgYnV2grx4FmJkk",
    authDomain: "chemie-da469.firebaseapp.com",
    databaseURL: "https://chemie-da469.firebaseio.com",
    projectId: "chemie-da469",
    storageBucket: "chemie-da469.appspot.com",
    messagingSenderId: "775983543184"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();