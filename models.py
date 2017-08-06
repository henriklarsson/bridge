from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'user_db1'
    id = Column(Integer, primary_key=True)
    pushId = Column(String(120), unique=False)
    pushType = Column(String(120), unique=False)
    bridgeType = Column(String(120), unique=False)


    def __init__(self, pushId, pushType, bridgeType):
        self.pushId = pushId
        self.pushType = pushType
        self.bridgeType = bridgeType

    def __str__(self):
        return ' STR <Id %r pushid: %r pushType %r bridetype: %r>' % (self.id, self.pushId, self.pushType, self.bridgeType)
    def __repr__(self):
        return 'REPR <Id %r pushid: %r pushType %r bridetype: %r>' % (self.id, self.pushId, self.pushType, self.bridgeType)