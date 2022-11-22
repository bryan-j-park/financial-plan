from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import bcrypt
from flask_app import EMAIL_REGEX
from flask_app.controllers.user_controller import bcrypt




from flask_app.models.transaction_models import Transaction


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("Bundle").query_db(query,data)

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("Bundle").query_db(query,data)
        print(results)
        if not results:
            return False
        else:
            print(results[0])
            return cls(results[0])


    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        results = connectToMySQL("Bundle").query_db(query,data)

        if not results:
            return False
        else:
            print(results[0])
            return cls(results[0])

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", "error_message_first_name")
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "error_message_last_name")
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email!","error_message_email")
            is_valid = False
        
        if (User.get_one_by_email(data)):
            flash("Email already in use!","error_message_email")
            is_valid = False
        
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', "error_message_password")
            is_valid = False
        
        if data['confirm_password'] != data['password']:
            flash('Passwords do not match!', "error_message_confirm_password")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        print(data['email'])
        found_user = User.get_one_by_email(data)
        if found_user:
            if not bcrypt.check_password_hash(found_user.password, data['password']):
                is_valid = False
        else:
            is_valid = False

        if not is_valid:
            flash("Invalid Login.")
