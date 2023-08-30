from os import stat
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask_app.models import user
from flask import flash

class Craft:
    db_name = 'asflights'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.code = db_data['code']
        #self.crafttype = db_data['crafttype']
        self.description = db_data['description']
        self.progress = db_data['progress']
        self.status = db_data['status']
        self.postedby_id = db_data['postedby_id']
        

    @classmethod # To insert data into the database
    def save(cls,data):
        query = "INSERT INTO asflight (code,description, progress, status,postedby_id) VALUES (%(code)s, %(description)s,%(progress)s,%(status)s,%(postedby_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod # To remove or delete a data from the database
    def destroy(cls,data):
        query = "DELETE FROM asflight WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def update(cls,data): # To edit an existing craft
        query = "UPDATE asflight SET code=%(code)s, description=%(description)s, progress=%(progress)s, status=%(status)s WHERE id = %(id)s;" # We only need to change certain fields, not all, so no need to include the postedby_id.
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls): # To run the query to obtain every single craft
        query = "SELECT * FROM asflight;"
        results = connectToMySQL(cls.db_name).query_db(query)
        asflight = []
        print("B"*50)
        print(results)
        for u in results:
            this_flight = cls(u)
            
            
            
            asflight.append( this_flight)
        return asflight



    @classmethod
    def get_one(cls,data): # To get one show
        query  = "SELECT * FROM asflight WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        deal = cls(result[0])
        
        # print("C"*50)
        # print(show)
        # print(show.releasedate)
        # print(type(show.releasedate))
        return deal

    @classmethod
    def get_postebyid(cls, data): # For the first and last name of the person who posted the song's id.
        query = "SELECT firstname, lastname FROM users  WHERE id = (Select postedby_id FROM asflight WHERE id=%(id)s );"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print("E"*50)
        print(result[0]["firstname"], result[0]["lastname"])
        return result[0]["firstname"] + " " + result[0]["lastname"]






    @staticmethod
    def validate_deal(deal):
        is_valid = True
        if len(deal['code']) < 1:
            is_valid = False
            flash("Please enter the code or flight number","deal")
        # if len(deal['crafttype']) < 1:
        #     is_valid = False
            #flash("Please enter the name of the artist(s)","deal")
        if len(deal['description']) < 1:
            is_valid = False
            flash("Please enter a description","deal")
        
        
        return is_valid
    

    # @staticmethod
    # def get_status(data):
    #     query = "SELECT * FROM status WHERE id = %(id)s;"
        
        
    #     results = connectToMySQL(Craft.db_name).query_db(query,data)
    #     stats = []
    #     print(results)
    #     for u in results:
    #         u["id"]    
    #         stats.append( u["status"])

    #     return stats

    # @staticmethod
    # def get_progress(data):
    #     query = "SELECT part FROM progress WHERE id = (SELECT progress_id FROM asflight WHERE id = %(id)s);"
        
        
    #     results = connectToMySQL(Craft.db_name).query_db(query,data)
    #     part = []
    #     print(results)
    #     # for u in results:
    #     #     u["id"]    
    #     #     part.append( u["part"])
    #     part.append(results)

    #     #print(part[0]["part"])
    #     return part

