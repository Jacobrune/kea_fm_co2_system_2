from mongoengine import Document, StringField, FloatField, IntField

class Product(Document):
    name = StringField(required=True)
    supplierId = StringField(required=True) 
    co2e = FloatField(required=True)
    price = FloatField()
