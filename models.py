"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.Text, nullable=False)

    size = db.Column(db.Text, nullable=False)

    rating = db.Column(db.Float, nullable=False)
    
    image = db.Column(db.Text, nullable=True, default="https://tinyurl.com/demo-cupcake")

    def serialize(self):
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_cupcakes(self):
        return [cupcake.serialize() for cupcake in Cupcake.query.order_by(Cupcake.flavor).all()]
    
