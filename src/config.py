import logging

# WARNING!
# This file will contain your PRIVATE Firebase credentials.
# DO NOT PUSH THIS FILE TO A REMOTE LOCATION
config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "/full/path/to/firebaseCredentials.json",
  "firebasePathPrefix": "test",
  "logLevel": logging.INFO,
  "exceptionRetries": 10
}
