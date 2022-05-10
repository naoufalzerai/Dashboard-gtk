from peewee import *
from DAL.UOW import BaseModel


class ProductType(BaseModel):
    name = CharField()


class Store(BaseModel):
    name = CharField()


class Product(BaseModel):
    name = CharField()
    inventory = IntegerField()
    type = ForeignKeyField(ProductType, backref='products')


class Invoice(BaseModel):
    store = ForeignKeyField(Store)
    date = DateTimeField()
    total = FloatField()


class InvoiceProducts(BaseModel):
    product = ForeignKeyField(Product)
    price = FloatField()
    quantity = IntegerField()
