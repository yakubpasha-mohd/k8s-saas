from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")
db = client["k8s_saas"]
clusters_collection = db["clusters"]
