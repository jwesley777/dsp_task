from peewee import *

db = SqliteDatabase(
    'bot.db'
)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    uid = IntegerField(primary_key=True)

class Voice(BaseModel):
    path = CharField(max_length=30)
    user = ForeignKeyField(User,backref='voices')
    
db.create_tables([User,Voice])