from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
#--------CLASS REVIEW
class Review:
#--------CONSTRUCTOR
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.company_id = data['company_id']
        self.title = data ['title']
        self.feedback = data['feedback']
        self.rate = data['rate']
        self.photo = data['photo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = ""
        self.sector = ""
        self.poster = ""

    #------CRUD
    #------READ ALL REVIEWS
    @classmethod
    def get_all(cls):
        query= """
        SELECT * FROM reviews ;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        rev = []
        for row in results:
            rev.append(cls(row))
        return rev

    #------CREATE REVIEW
    @classmethod
    def add_review(cls, data):
        query = """
        INSERT INTO reviews (user_id, company_id, title, feedback, rate, photo) 
        VALUES (%(user_id)s, %(company_id)s, %(title)s, %(feedback)s, %(rate)s, %(photo)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    #----------UPDATE REVIEW
    @classmethod
    def edit_review(cls, data):
        query = """
        UPDATE reviews SET title= %(title)s ,feedback=%(feedback)s, rate=%(rate)s, photo=%(photo)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
        
    #----------DELETE COMPANY
    @classmethod
    def delete_review(cls, data):
        query = """
        DELETE FROM reviews where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    #---------GET BY ID
    @classmethod
    def get_by_id(cls,data):
        query= """
        SELECT * FROM reviews WHERE id= %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    #---------GET BY ID
    @classmethod
    def get_by_user_id(cls,data):
        query= """
        SELECT reviews.id, reviews.user_id, reviews.company_id, reviews.feedback, reviews.rate, 
        reviews.photo, reviews.created_at, reviews.updated_at, 
        reviews.title AS title, companies.name AS name, sectors.title AS sector
        FROM reviews
        JOIN companies ON company_id = companies.id
        JOIN sectors ON sector_id = sectors.id
        WHERE reviews.user_id= %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        reviews  = []
        if results:
            for row in results:
                rev = cls(row)
                rev.sector = row["sector"]
                rev.name = row["name"]
                reviews.append(rev)
        return reviews
    
    @classmethod
    def get_company_reviews(cls, data):
        query="""
        SELECT reviews.*, users.pseudo AS poster
        FROM reviews
        LEFT JOIN users ON user_id = users.id
        WHERE reviews.company_id= %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        reviews  = []
        if results:
            for row in results:
                rev = cls(row)
                rev.poster = row["poster"]
                reviews.append(rev)
        return reviews
    
    @classmethod
    def get_company_avg(cls, data):
        query="""
        SELECT AVG(rate) as rate FROM reviews
        WHERE company_id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result[0]['rate'] == None:
            return 0
        else:
            return "{:.2f}".format(result[0]['rate'])
    
    @classmethod
    def count(cls):
        query="SELECT COUNT(*) as reviews_number FROM reviews;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result[0]['reviews_number']
    