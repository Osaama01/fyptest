from app import db

class CUSTOMERS(db.Model):
    __tablename__ = "CUSTOMERS"
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120))
    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    contact_no = db.Column(db.String(120))

    def __init__(self, customer_id=None, customer_name=None, country=None, city=None, contact_no=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.country=country
        self.city=city
        self.contact_no=contact_no
