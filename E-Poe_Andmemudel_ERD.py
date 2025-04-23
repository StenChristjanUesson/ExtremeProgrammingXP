from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    client_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String)
    address = Column(String)
    
    orders = relationship('Order', back_populates='client')

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date)
    delivery_address = Column(String)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    
    products = relationship('Product', secondary='order_products')
    payment = relationship('Payment', back_populates='order')
    
    client = relationship('Client', back_populates='orders')

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    
    category = relationship('Category', back_populates='products')
    
    orders = relationship('Order', secondary='order_products')
    
    stock = relationship('Stock', back_populates='product', uselist=False)

class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    
    products = relationship('Product', back_populates='category')

class Payment(Base):
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True)
    payment_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    
    order = relationship('Order', back_populates='payment')

class Stock(Base):
    __tablename__ = 'stocks'
    
    stock_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    
    product = relationship('Product', back_populates='stock')

class OrderProduct(Base):
    __tablename__ = 'order_products'
    
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)

engine = create_engine('sqlite:///ecommerce.db', echo=True)

Base.metadata.create_all(engine)

# Ja siin on andmete lisamise näide:

python
Copy
Edit
from sqlalchemy.orm import sessionmaker
from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

new_client = Client(name="John Doe", email="john@example.com", phone="123456789", address="123 Main St")
session.add(new_client)

new_category = Category(category_name="Electronics")
session.add(new_category)

new_product = Product(name="Smartphone", price=299.99, category=new_category)
session.add(new_product)

new_order = Order(order_date=date.today(), delivery_date=date.today(), delivery_address="123 Main St", client=new_client)
session.add(new_order)

new_payment = Payment(payment_date=date.today(), amount=299.99, status="Completed", order=new_order)
session.add(new_payment)

new_stock = Stock(quantity=100, product=new_product)
session.add(new_stock)

session.commit()
session.close()
