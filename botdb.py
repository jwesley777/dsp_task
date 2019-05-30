from peewee import *

db = SqliteDatabase(
    'bot.db'
)

class BaseModel(Model):
    class Meta:
        database = db

# User model
class User(BaseModel):
    uid = IntegerField(primary_key=True) #user id

# Voice message model
class Voice(BaseModel):
    path = CharField(max_length=30) # path to audiofile on disk
    user = ForeignKeyField(User,backref='voices') # user id
    
db.create_tables([User,Voice])