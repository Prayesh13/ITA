from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,PyMongoError

# establish connection to MongoDB local server

class MyDB():

    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['ITA']
        except ConnectionFailure as e:
            print(f"Couldn't connect to Database: {e}")
        else:
            print('Successfully connected to Database!')
            self.collection = self.db['user']
            print("Ayya bhi!!")

    def insert_one_data(self, username, email, gender, dob, password):
        try:
            data = {
                'username': username,
                'email': email,
                'gender': gender,
                'dob': dob,
                'password': password
            }
            # Use insert_one for a single document
            self.collection.insert_one(data)
            return "Data Inserted Successfully!"
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return "Couldn't insert data into Database"

    def search(self, email, password):
        try:
            # Query for the user with the given email
            user = self.collection.find_one({'email': email})

            # Check if user exists and password matches
            if user and user.get('password') == password:
                return 1  # Success
            else:
                return 0  # Failure
        except PyMongoError as e:
            print(f"An error occurred during search: {e}")
            return 0