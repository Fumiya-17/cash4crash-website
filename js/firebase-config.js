const firebaseConfig = {
  apiKey:            "AIzaSyBiTs1bz0UwFpQ6X15gWvBYXNFLeJiLUks",
  authDomain:        "cash4crash-c9fcd.firebaseapp.com",
  projectId:         "cash4crash-c9fcd",
  storageBucket:     "cash4crash-c9fcd.firebasestorage.app",
  messagingSenderId: "529034294123",
  appId:             "1:529034294123:web:77943157c0cfc5cef7122e",
  measurementId:     "G-4MPKZMDEBJ"
};

// Initialize Firebase only if it hasn't been initialized yet
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}
const auth = firebase.auth();
