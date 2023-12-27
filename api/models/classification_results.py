from ..utils import db
from datetime import datetime

class ClassificationResult(db.Model):
    __tablename__='classification_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(255), nullable=False)
    result_value = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Classifucation {self.id}>"