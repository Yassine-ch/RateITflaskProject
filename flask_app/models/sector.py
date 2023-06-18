from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
#--------CLASS SECTOR
class Sector:
#--------CONSTRUCTOR
    def init(self,data):
        self.id = data['id']
        self.title = data['title']
        self.logo = data['logo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
#------CRUD

    #------READ ALL SECTORS
    @classmethod
    def get_all(cls):
        query= """
        SELECT * FROM sectors ;
        """
        return connectToMySQL(DATABASE).query_db(query) 

    #------CREATE SECTOR
    @classmethod
    def add_sector(cls, data):
        query = """
        INSERT INTO sectors (title, logo) 
        VALUES (%(title)s,%(logo)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    #----------UPDATE SECTOR
    @classmethod
    def edit_sector(cls, data):
        query = """
        UPDATE sectors SET title = %(title)s, logo = %(logo)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    #----------DELETE SECTOR
    @classmethod
    def delete_sector(cls,data):
        query = """
        delete from sectors where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #---------GET BY ID
    @classmethod
    def get_by_id(cls,data):
        query= """
        SELECT * FROM sectors WHERE id= %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result[0]


    @classmethod
    def count(cls):
        query="SELECT COUNT(*) AS sectors_number FROM sectors;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result[0]['sectors_number']