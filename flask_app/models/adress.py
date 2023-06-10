from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Adress:
    def __init__(self,data):
        self.id=data['id']
        self.city_ID=data['city_ID']
        self.number=data['number']
        self.street=data['street']
        self.zipcode=data['zipcode']
        self.created_at=data['created_at']
        self.updated_at=data['updqted_at']
    
    @classmethod
    def add_adress(cls, data):
        query = """
        INSERT INTO adresses (city_ID, number, street, zipcode) 
        VALUES (%(city_ID)s,%(number)s, %(street)s, %(zipcode)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
        