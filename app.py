from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from config import Config
from models import db, Product, ServiceRequest, Order, OrderItem, Admin
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)


# Home
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    return render_template('index.html', products=products)


# Products listing
@app.route('/products')
def products():
    q = request.args.get('q')
    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
        items = query.all()
    return render_template('products.html', products=items)


# Product detail
@app.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    return render_template('product_detail.html', product=p)


# Service booking
@app.route('/book-service', methods=['POST'])
def book_service():
    data = request.form
    sr = ServiceRequest(
    customer_name=data.get('name'),
    phone=data.get('phone'),
    email=data.get('email'),
    address=data.get('address'),
    service_type=data.get('service_type'),
    preferred_date=data.get('preferred_date'),
    notes=data.get('notes')
)
    db.session.add(sr)
    db.session.commit()
# You can add SMS/WhatsApp/Email notification here
    flash('Service request submitted. We will call you soon!')
    return redirect(url_for('index'))


# Simple REST endpoint for products (for JS)
@app.route('/api/products')
def api_products():
    prods = Product.query.all()
    out = []
    for p in prods:
        out.append({'id':p.id,'name':p.name,'price':str(p.price),'image':p.image or ''})
    return jsonify(out)
app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
