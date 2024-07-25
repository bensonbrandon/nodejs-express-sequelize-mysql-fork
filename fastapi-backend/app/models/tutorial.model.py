from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tutorial(Base):
    __tablename__ = 'tutorial'

    title = Column(String)
    description = Column(String)
    published = Column(Boolean)

# Example of how to create an engine and session
# engine = create_engine('sqlite:///tutorial.db')
# Session = sessionmaker(bind=engine)
# session = Session()
