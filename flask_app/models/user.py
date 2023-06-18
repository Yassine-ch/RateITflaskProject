from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#--------CLASS USER
class User :
#--------CONSTRUCTOR
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.pseudo = data['pseudo']
        self.email = data['email']
        self.password = data['password']
        self.avatar = data['avatar']
        self.is_admin =data['is_admin']
        self.actif = data['actif']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
#--------CRUD

#--------Read All Users
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM users;
        """
        result = connectToMySQL(DATABASE).query_db(query)
        results =[]
        for row in result:
            results.append(cls(row))
        return results
        
    
#--------Create USER
    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, pseudo, email, password, avatar) 
        VALUES (%(first_name)s, %(last_name)s, %(pseudo)s, %(email)s, %(password)s, %(avatar)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    def __repr__(self) -> str:
        return f"{self.first_name}--{self.last_name}--{self.email}"
    
    @classmethod
    def update_user(cls,data):
        query="""
        UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s,pseudo= %(pseudo)s,email = %(email)s, password = %(password)s, avatar = %(avatar)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    #--------GET BY ID
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    #--------GET BY EMAIL
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if(result):
            return cls(result[0])
        return False
    

    @classmethod
    def count(cls):
        query="SELECT COUNT(*) AS users_number FROM users;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result[0]['users_number']

    
    #--------VALIDATION
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])< 2:
            flash("First Name must be at least 3 caracters","Register")
            is_valid = False
        if len(data['last_name'])< 2:
            flash("Last name is required","Register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","Register")
            is_valid = False
        elif User.get_by_email({'email':data['email']}):
            flash("Email address already used, try login","Register")
            is_valid = False
        if len(data['password'])< 6:
            flash("Password too short","Register")
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("Password does not match ","Register")
            is_valid = False
        return is_valid