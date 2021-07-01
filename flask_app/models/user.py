from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.band import Band
import re
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__( self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bands = [] # bands that a user has joined
        self.all_bands = []
        self.mybands = []


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL("band_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN bands ON users.id = bands.user_id WHERE users.id=%(id)s;"
        results = connectToMySQL("band_schema").query_db(query,data)

        user = cls(results[0])

        if results[0]['bands.id'] != None:
            for row in results:
                row_data = {
                    "id":row['bands.id'], # conflicting dictionary keys need table specified
                    "name":row['name'],
                    "genre":row['genre'],
                    "home_city":row['home_city'],
                    "created_at":row['bands.created_at'],
                    "updated_at":row['bands.updated_at'],
                    "user":user
                }
                user.bands.append(Band(row_data))
        query = "SELECT id,name,genre,home_city,user_id FROM bands;"
        results = connectToMySQL("band_schema").query_db(query)

        if len(results)>0:
            for band in results:
                user.all_bands.append(band['id'])
        return user


    @classmethod
    def insert(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL("band_schema").query_db(query,data)


    @classmethod
    def one_user_bands(cls,data):
        query = "SELECT * FROM users LEFT JOIN members ON users.id=members.user_id LEFT JOIN bands ON bands.id=members.band_id WHERE users.id=%(id)s;"
        results = connectToMySQL("band_schema").query_db(query,data)

        user = cls(results[0])
        if results[0]['bands.id'] != None:
            for row in results:
                row_data = {
                    "id":row['bands.id'], # conflicting dictionary keys need table specified
                    "name":row['name'],
                    "genre":row['genre'],
                    "home_city":row['home_city'],
                    "created_at":row['bands.created_at'],
                    "updated_at":row['bands.updated_at'],
                    "user":user
                }
                user.bands.append(Band(row_data))
        return user
    
    @classmethod
    def join(cls,data):
        query = "INSERT INTO members(user_id,band_id) VALUES(%(user_id)s,%(band_id)s);"
        return connectToMySQL('band_schema').query_db(query,data)


    @staticmethod  # make sure no duplicate email # has email structure
    def validate_user(data):
        print(f'################ {data}')
        is_valid = True # the keys must match the request.form keys or NAME in the HTML
        if len(data['first_name']) < 3:
            flash("Name must be at least 3 characters.",'name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("last must be at least 3 characters.","name")
            is_valid = False
        if not data['first_name'].isalpha():
            flash("May not contain non alphabetical characters","name")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!",'emailError')
            is_valid = False
        print(data['email'])
        if User.duplicates(data['email']):
            flash("Invalid email address!",'emailError')
            is_valid = False
        if len(data['password']) < 8:
            flash("password must be at least 3 characters.","password")
            is_valid = False
        if data['password'] != data['confirm']:
            flash("Passwords must Match","confirm")
        flash(f"You have successfully logged in with : {data['email']}","success")
        return is_valid


    @staticmethod  # make sure no duplicate email # has email structure
    def validate_create(data):
        is_valid = True # the keys must match the request.form keys or NAME in the HTML
        if len(data['name']) < 2:
            flash("Must be at least 1 character long.")
            is_valid = False
        if len(data['genre']) < 2:
            flash("Please enter genre")
            is_valid = False
        if data['home_city'] =='':
            flash("Must include home town")
            is_valid = False
        return is_valid


    @staticmethod
    def duplicates(email):
        query = f"SELECT email FROM users WHERE email='{email}';"
        result = connectToMySQL('band_schema').query_db(query)

        duplicate = False
        if result:
            duplicate = True
        return duplicate