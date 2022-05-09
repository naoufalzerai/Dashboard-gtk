from peewee import *
from DAL.UOW import BaseModel


class ProductType(BaseModel):
    # id = UUIDField(primary_key=True)
    name = CharField()
