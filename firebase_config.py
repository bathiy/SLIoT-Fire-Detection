import pyrebase

# Firebase project config
firebaseConfig = {
    "apiKey": "AIzaSyD30B-XphgHNt9V_Mfk_49cHOZEiB3IRX0",
    "authDomain": "fire-detection-system-cbd08.firebaseapp.com",
    "databaseURL": "https://fire-detection-system-cbd08-default-rtdb.firebaseio.com",
    "projectId": "fire-detection-system-cbd08",
    "storageBucket": "fire-detection-system-cbd08.appspot.com",
    "messagingSenderId": "362077776927",
    "appId": "1:362077776927:android:4dcd0201fdb1c485c6f92a"
}

# Initialize
firebase = pyrebase.initialize_app(firebaseConfig)

# Export db and storage for others
db = firebase.database()
storage = firebase.storage()
