from jupyterhub.orm import Base
from sqlalchemy import Column, Integer, String


class UserKeyInfo(Base):
    __tablename__ = "user_keys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    private_key = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    certificate = Column(String, nullable=False)
    fingerprint = Column(String, nullable=False)
    username = Column(String(128), nullable=False)

    @classmethod
    def find(cls, db, username):
        return db.query(cls).filter(cls.username == username).first()
