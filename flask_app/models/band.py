from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bands;"
        results = connectToMySQL('band_schema').query_db(query)
        bands = []
        if len(results)>0:
            for band in results:
                data = {
                    "id":band['id'],
                    "name":band['name'],
                    "genre":band['genre'],
                    "home_city":band['home_city'],
                    "created_at":band['created_at'],
                    "updated_at":band['updated_at'],
                    "user":user.User.get_by_id({"id":band['user_id']}) # 
                }
                bands.append(cls(data))
                
            return bands


    # need to figure out what the joining table keys stand for and how we are classifying people in bands
    @classmethod
    def get_members(cls,data):
        query = "SELECT band_id FROM members WHERE user_id=%(id)s;"
        results = connectToMySQL("band_schema").query_db(query,data)
        print(f'############{results}')
        bands = []
        if results != None:
            for band in results:
                bands.append(band['band_id'])

        return bands

    

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM bands WHERE id=%(id)s;"
        results = connectToMySQL('band_schema').query_db(query,data)
        one_band = {
            "id":results[0]['id'],
            "name":results[0]['name'],
            "genre":results[0]['genre'],
            "home_city":results[0]['home_city'],
            "created_at":results[0]['created_at'],
            "updated_at":results[0]['updated_at'],
            "user":user.User.get_by_id({"id":results[0]['user_id']})
        }
        return cls(one_band)


    @classmethod
    def insert_band(cls,data):
        query = "INSERT INTO bands (name,genre,home_city,created_at, updated_at,user_id) VALUES(%(name)s,%(genre)s,%(home_city)s,NOW(), NOW(),%(user_id)s);"
        return connectToMySQL('band_schema').query_db(query,data)


    @classmethod
    def update_band(cls,data):

        query = "UPDATE bands SET name=%(name)s,genre=%(genre)s,home_city=%(home_city)s,created_at=NOW(), updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('band_schema').query_db(query,data)


    # @classmethod
    # def join(cls,data):
    #     query = "INSERT INTO members(user_id,band_id) VALUES(%(user_id)s,%(band_id)s);"
    #     return connectToMySQL('band_schema').query_db(query,data)


    @classmethod # deleting bands
    def delete(cls,data):
        query = "DELETE FROM bands WHERE id=%(id)s"
        return connectToMySQL('band_schema').query_db(query,data)


    @classmethod # quiting joined bands (deleting rows in members joining table)
    def quit(cls,data):
        query = "DELETE FROM members WHERE user_id=%(user_id)s AND band_id=%(band_id)s;" # we need the band_id in members
        connectToMySQL('band_schema').query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bands;"
        results = connectToMySQL('band_schema').query_db(query)
        bands = []
        if len(results)>0:
            for band in results:
                data = {
                    "id":band['id'],
                    "name":band['name'],
                    "genre":band['genre'],
                    "home_city":band['home_city'],
                    "created_at":band['created_at'],
                    "updated_at":band['updated_at'],
                    "user":user.User.get_by_id({"id":band['user_id']}) # 
                }
                bands.append(cls(data))
            return bands