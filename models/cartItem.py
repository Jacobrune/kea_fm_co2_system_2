from mongoengine import EmbeddedDocument, ObjectIdField, IntField

class CartItem(EmbeddedDocument):
    product_id = ObjectIdField(required=True)
    quantity = IntField(required=True)
