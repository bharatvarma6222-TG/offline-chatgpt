from sqlalchemy import Column, Integer, String, Text

from backend.database.db import Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(String, index=True)

    role = Column(String)

    content = Column(Text)
