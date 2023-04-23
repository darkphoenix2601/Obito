from motor.motor_asyncio import AsyncIOMotorClient as ObitoMongoClient
from Obito import MONGO_DB_URI, mongo

Obitomongo = ObitoMongoClient(MONGO_DB_URI)
Obitodb = Obitomongo.szrose

#Indexes for Plugins
coupledb = Obitodb.couple
karmadb = Obitodb.karma
nsfwdb = Obitodb.nsfw
chatbotdb = Obitodb.chatbot
torrentdb = Obitodb.torrentdb
AIbotdb = Obitodb.AIbotdb
