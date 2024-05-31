from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = 'mongodb://localhost:27017/'

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.todos #database name

todo_collection = database.get_collection("todo_collection")

