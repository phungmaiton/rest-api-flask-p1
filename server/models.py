# Import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# 6. Import `SerializerMixin` from `sqlalchemy_serializer`

# Initialize our db
db = SQLAlchemy()

# 7. Pass `SerializerMixin` to your model(s)
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # NOTE added this between day 1 and day 2
    shows = db.relationship('Show', backref='service')

    # 7.1 Create a serialize rule that will help add our shows to the services response
        # This is a tuple, so if there's only one item, you need the trailing comma or it will yell

    def __repr__(self):
        return f"<Service Name: {self.name}, Price: ${self.price}>"

# NOTE added this between day 1 and day 2
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    seasons = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # 8. Create a serialize rule that will add our 'service' to the shows response

    def __repr__(self):
        return f'<Show Name: {self.name}, seasons: ${self.seasons}>'

# 9. back to app.py to implement