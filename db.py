import os
# import certifi
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bson import ObjectId
from dotenv import load_dotenv
import datetime
import traceback

import json

load_dotenv()

# Database Setup
conn_str = os.getenv("CONNECTION_STRING")
database_name = os.getenv("DATABASE_NAME")
# client = MongoClient("", tlsCAFile=certifi.where())
client = MongoClient(conn_str)
db = client[database_name]

# User wrapper class for Flask-Login
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.name = user_doc.get('name', '')
        self.email = user_doc.get('email', '')
        self.contact = user_doc.get('contact', '')
        self.pw_hash = user_doc.get('password', '')
        self.role = user_doc.get('role', 'user')

    def check_password(self, password, bcrypt):
        return bcrypt.check_password_hash(self.pw_hash, password)

        # Helper property to check if user is an admin

    @property
    def is_admin(self):
        print(self.role, "role")
        return self.role == 'admin'

        # Static loader method by User ID (for Flask-Login @login_manager.user_loader)

    @staticmethod
    def get_by_id(user_id):
        try:
            user_doc = db.user.find_one({'_id': ObjectId(user_id)})
            return User(user_doc) if user_doc else None
        except Exception:
            return None

    # Static loader method by Email
    @staticmethod
    def get_by_email(email):
        user_doc = db.user.find_one({'email': email})
        return User(user_doc) if user_doc else None

    # @staticmethod
    # def get_password(email):
    #     result = db.user.find_one({'email': email})
    #     password = ''
    #     if result:
    #         for data in result:
    #             name = data['name']
    #             password = data['password']
    #             print('password in db class', password)
    #     return password

    @staticmethod
    def insert_id(user_id):
        try:
            user_doc = db.user.find_one({'_id': ObjectId(user_id)})
            return User(user_doc) if user_doc else None
        except Exception:
            return None

    @staticmethod
    def add_user(name, email, contact, pw_hash):
        try:
            ts = datetime.datetime.today().strftime("%a %b %d %X  %Y")
            rec = {
                'name': name,
                'email': email,
                'contact': contact,
                'password': pw_hash,
                'role': 'user',
                'creation_date': ts
            }
            return db.user.insert_one(rec)
        except Exception:
            return None

        # except Exception as exp:
        #     print("add_user() :: Got exception: %s", exp)
        #     print(traceback.format_exc())


#
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


# User wrapper class for Flask-Login
# class User(UserMixin):
#     def __init__(self, user_doc):
#         self.id = str(user_doc['_id'])
#         self.name = user_doc.get('name')
#         self.email = user_doc.get('email')
#         self.pw_hash = user_doc.get('pw_hash')
#
#     @staticmethod
#     def get_by_id(user_id):
#         try:
#             user_doc = db.user.find_one({'_id': ObjectId(user_id)})
#             return User(user_doc) if user_doc else None
#         except Exception:
#             return None
#
#     @staticmethod
#     def get_by_email(email):
#         user_doc = db.user.find_one({'email': email})
#         return User(user_doc) if user_doc else None


# class Mdb:
#     def __init__(self):
#         db_name = "swastik_db"
#         conn_str = os.getenv("CONNECTION_STRING")
#         client = MongoClient(conn_str)
#         self.db = client[db_name]
#
# #############################################
# #                                           #
# #                GET LAST ID                #
# #                                           #
# #############################################
#     def get_last_id(self):
#         data = self.db.user.find({}).count() > 0
#         if data == True:
#             last_id = self.db.user.find({}).sort({"_id": -1}).limit(1)
#         else:
#             last_id = 0
#         return last_id
#
# #################################################
# #                                               #
# #                    ADD_USER                   #
# #                                               #
# #################################################
#     def add_user(self, name, email, contact, pw_hash):
#         try:
#             ts = datetime.datetime.today().strftime("%a %b %d %X  %Y ")
#             rec = {
#                 'name': name,
#                 'email': email,
#                 'contact': contact,
#                 'password': pw_hash,
#                 'role': '',
#                 'creation_date': ts
#             }
#             self.db.user.insert_one(rec)
#         except Exception as exp:
#             print("add_user() :: Got exception: %s", exp)
#             print(traceback.format_exc())
#
# #############################################
# #                                           #
# #           CHECK USER IN DATABASE          #
# #                                           #
# #############################################
#     def user_exists(self, email):
#         return self.db.user.count_documents({'email': email}) > 0
#
# #############################################
# #                                           #
# #               GET NEW PASSWORD            #
# #                                           #
# #############################################
#     def get_data_by_email(self, email):
#         result = self.db.user.find({'email': email})
#         name = ''
#         password = ''
#         if result:
#             for data in result:
#                 name = data['name']
#                 password = data['password']
#                 print ('password in db class', password)
#         return password
#
# #############################################
# #                                           #
# #        GET NAME ACCORDING TO EMAIL        #
# #                                           #
# #############################################
#     def get_name(self, email):
#         result = self.db.user.find_one({'email': email})
#         name = ''
#         email = ''
#         if result:
#             for data in result:
#                 name = data['name']
#                 email = data['email']
#         return name
#
# #############################################
# #                                           #
# #            USER SESSION IN DATABASE       #
# #                                           #
# #############################################
#     def save_login_info(self, user_email, mac, ip, user_agent, LOGIN_TYPE):
#         # LOGIN_TYPE = 'User Login'
#         try:
#             ts = datetime.datetime.today().strftime("%a %b %d %X  %Y ")
#             rec = {
#                 'user_id': user_email,
#                 'mac': mac,
#                 'ip': ip,
#                 'user_agent': user_agent,
#                 'user_type': LOGIN_TYPE,
#                 'timestamp': ts
#             }
#             self.db.user_session.insert(rec)
#         except Exception as exp:
#             print( "save_login_info() :: Got exception: %s", exp)
#             print(traceback.format_exc())
#
# #############################################
# #                                           #
# #                 GET SESSION               #
# #                                           #
# #############################################
#     def get_sessions(self):
#         collection = self.db["user_session"]
#         result = collection.find({})
#         ret = []
#         for data in result:
#             ret.append(data)
#         return ret
#
# #############################################
# #                                           #
# #         GET USER ID BY SESSION            #
# #                                           #
# #############################################
#     def get_user_id_by_session(self, email):
#         result = self.db.user.find({'email': email})
#         id = ''
#         if result:
#             for data in result:
#                 id = data['_id']
#         return id
#
# #############################################
# #                                           #
# #               OR Query                    #
# #                                           #
# #############################################
#     def search_user(self, text):
#         result = self.db.user.find({
#             "$or":
#                 [
#                     # {"title": text}
#                     # {"title" : { "$regex" : ".*${text}.*"} }
#                     {'email': {'$regex': text, '$options': 'i'}}
#                  ]
#         })
#         # ret = []
#         for user in result:
#             return user
#             # ret.append(user)
#         # return ret
#
#     # db.survey.find( { $or:[ {"title": "Help Survey"} ] } )
#
# ##############################################
# #                                            #
# #       GET SECURITY QUESTION BY EMAIL       #
# #                                            #
# ##############################################
#     def get_security_question(self, email):
#         result = self.db.user.find({'email': email})
#         question = ''
#         if result:
#             for data in result:
#                 question = data['question']
#                 print ('password in db class', question)
#         return question
#
#     def get_security_answer(self, email):
#         result = self.db.user.find({'email': email})
#         answer = ''
#         if result:
#             for data in result:
#                 answer = data['answer']
#                 print ('password in db class', answer)
#         return answer
#
#     def set_password(self, email, pw_hash):
#         self.db.user.update(
#             {'email': email},
#             {'$set': {'password': pw_hash}},
#             upsert=True, multi=True)
#
# #################################################
# #                                               #
# #                    ADD_TODO                   #
# #                                               #
# #################################################
#     def add_todo(self, title, description, date, status, email):
#         try:
#             ts = datetime.datetime.today().strftime("%a %b %d %X  %Y ")
#             rec = {
#                 'title': title,
#                 'description': description,
#                 'date': date,
#                 'status': status,
#                 'email': email,
#                 'creation_date': ts
#             }
#             self.db.todo.insert(rec)
#         except Exception as exp:
#             print ("add_todo() :: Got exception: %s", exp)
#             print(traceback.format_exc())
#
#
# #################################################
# #                                               #
# #                get_all_todo                   #
# #                                               #
# #################################################
#     def get_all_user(self):
#         collection = self.db["user"]
#         result = collection.find({})
#
#         ret = []
#         for data in result:
#             ret.append(data)
#         return JSONEncoder().encode({'users': ret})
#
# #################################################
# #                                               #
# #                 Delete user                   #
# #                                               #
# #################################################
#     def delete_user(self, email):
#         ret = []
#         collection = self.db["user"]
#         collection.remove({"email": email})
#         todo_collection = self.db["todo"]
#         todo_collection.remove({"email":email})
#         result = collection.find({})
#         for data in result:
#             ret.append(data)
#         return JSONEncoder().encode({'users': ret})
#
# #################################################
# #                                               #
# #            get_all_pending_todo               #
# #                                               #
# #################################################
#     def get_all_pending(self, email):
#         ret = []
#         collection = self.db["todo"]
#         result = collection.find({"status": "0", "email": email})
#         # if not result:
#         #     not_done = collection.find()
#         #     for data in not_done:
#         #         print "<<=====got the data====>> :: %s" % data
#         #         ret.append(data)
#         #     return JSONEncoder().encode({'todo': ret})
#
#         for data in result:
#             ret.append(data)
#         return JSONEncoder().encode({'todo': ret})
#
# #################################################
# #                                               #
# #             get_all_done_todo                 #
# #                                               #
# #################################################
#     def get_all_complete(self, email):
#         ret = []
#         collection = self.db["todo"]
#         result = collection.find({"status": "1", "email": email})
#         # if not result:
#         #     not_done = collection.find()
#         #     for data in not_done:
#         #         print "<<=====got the data====>> :: %s" % data
#         #         ret.append(data)
#         #     return JSONEncoder().encode({'todo': ret})
#
#         for data in result:
#             ret.append(data)
#         return JSONEncoder().encode({'todo': ret})


if __name__ == "__main__":
    mdb = Mdb()