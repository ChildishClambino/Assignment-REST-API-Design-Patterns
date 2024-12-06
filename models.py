from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(50))  # Ensure this matches your intent
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    customer_id = db.Column(db.Integer)
    total_value = db.Column(db.Float)
    date = db.Column(db.Date)


    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.employee_name,
            'quantity': self.quantity,
            'product_id': self.product_id,
            'customer_id': self.customer_id,
            'total_value': self.total_value,
            'date': self.date,
            # other fields...
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # other fields...

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # other fields...
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Production(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    date_produced = db.Column(db.Date, nullable=False)