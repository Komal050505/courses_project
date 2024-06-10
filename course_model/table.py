
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# CREATE A DATABASE TABLE MODEL
class Courses(Base):
    __tablename__ = "courses"

    name = Column("course_name", String(50), primary_key=True)
    fee = Column("course_fee", Integer)
    part_time = Column("is_part_time", Boolean)
    full_time = Column("is_full_time", Boolean)
    weeks = Column("no_of_weeks", Integer)
    online = Column("is_online", Boolean)
    inperson = Column("is_inperson", Boolean)
