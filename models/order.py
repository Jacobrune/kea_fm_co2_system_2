from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, IntField
from datetime import datetime

class OrderItem(EmbeddedDocument):
    product_name = StringField(required=True)
    quantity = IntField(required=True)

class Order(Document):
    items = ListField(EmbeddedDocumentField(OrderItem))
    status = StringField(default="Pending")  
    created_at = StringField(default=lambda: datetime.utcnow().isoformat())