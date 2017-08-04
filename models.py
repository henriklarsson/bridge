from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'userzs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=False)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r id: %r>' % (self.name, self.id)