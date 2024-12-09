from flask import Flask, request, redirect, url_for, render_template, session
from models.product import Product
from models.cartItem import CartItem
from models.order import Order, OrderItem
import secrets
from mongoengine import connect, Document, StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField

class FlaskApp:
    def __init__(self, config=None):
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_hex(16) 
        connect(host="mongodb+srv://admin:V0gvOlZ6owmLwyk4@cluster0.6mxos.mongodb.net/KeaFm?retryWrites=true&w=majority")
        self.add_routes()

    def add_routes(self):
        @self.app.route('/')
        def home():
            return render_template('home.html')
        
        @self.app.route('/set-role', methods=['POST'])
        def set_role():
            role = request.form.get('role')

            session['role'] = role

            if role == 'admin':
                return redirect('/orders')  
            elif role == 'cleaningpersonal':
                return redirect('/products')  

        
        @self.app.route('/products')
        def product_list():
            products = Product.objects()  
            return render_template('productList.html', products=products)
        
        @self.app.route('/add-to-cart', methods=['POST'])
        def add_to_cart():
            product_id = request.form.get('product_id')

            product = Product.objects(id=product_id).first()
            if not product:
                return "Product not found", 404


            cart = session.get('cart', [])
            cart.append({
                'product_id': str(product.id),
                'name': product.name,
                'quantity': 1
            })
            session['cart'] = cart

            return redirect('/products')  

        @self.app.route('/admin')
        def admin():
            return "nej"

        @self.app.route('/cart')
        def cart():
            cart = session.get('cart', [])
            return render_template('cart.html', cart=cart)
        
        @self.app.route('/place-order', methods=['POST'])
        def place_order():
            cart = session.get('cart', [])
            if not cart:
                return "Cart is empty. Cannot place order.", 400
            
            order_items = [OrderItem(product_name=item['name'], quantity=item['quantity']) for item in cart]

            order = Order(items=order_items)
            order.save()

            session['cart'] = []

            return redirect('/orders')

        @self.app.route('/orders')
        def orders():
            all_orders = Order.objects()
            return render_template('orders.html', orders=all_orders)
        
        @self.app.route('/approve-order/<order_id>', methods=['POST'])
        def approve_order(order_id):
            if session.get('role') != 'admin':
                return "Access denied", 403

            order = Order.objects(id=order_id).first()
            if not order:
                return "Order not found", 404

            order.status = "Approved"
            order.save()
            return redirect('/orders')

        @self.app.route('/reject-order/<order_id>', methods=['POST'])
        def reject_order(order_id):
            if session.get('role') != 'admin':
                return "Access denied", 403

            order = Order.objects(id=order_id).first()
            if not order:
                return "Order not found", 404

            order.status = "Rejected"
            order.save()
            return redirect('/orders')

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(host=host, port=port)


if __name__ == "__main__":
    app = FlaskApp()
    app.run()
