import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


class Image:
        def __init__(self, user_id, path_to_img):
                self.user_id = user_id
                self.path_to_img = path_to_img
        
        @classmethod
        def find_by_id(cls, _id):
                #method to return a User object on None querying from database
                client = MongoClient('localhost',27017)
                db = client['test-user-db-memory-lane']
                collection = db['test-image-collection']



                result = collection.find_one({'_id': ObjectId(_id)})

                client.close()
                if result:
                        return cls(result['user_id'], result['path_to_img'])
                else:
                        return None, None


        @classmethod
        def find_by_path(cls, path_to_img):
                #method to return a User object on None querying from database
                client = MongoClient('localhost',27017)
                db = client['test-user-db-memory-lane']
                collection = db['test-image-collection']



                result = collection.find_one({'path_to_img': path_to_img})

                client.close()
                if result:
                        return str(result['_id'])
                else:
                        return None


        def insert(self):
                # print('Hello World')
                client = MongoClient('localhost',27017)
                db = client['test-user-db-memory-lane']
                collection = db['test-image-collection']

                post = {
                        "user_id": self.user_id,
                        "path_to_img": self.path_to_img
                }
                try:
                        if collection.insert_one(post) == None:
                                client.close()
                                return False
                        else:
                                client.close()
                                return True
                except:
                        client.close()
                        return False


