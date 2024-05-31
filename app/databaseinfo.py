from databaseconnector import MongoDBClient, DBConnect

client = MongoDBClient("localhost", 27017, "todos", "todo_collection")
db = DBConnect(client)

db.connect()