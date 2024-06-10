from course_model.table import Courses
from course_db_connections.configurations import session


def is_course_exist(name):
    """
    This function return True if course exists False otherwise
    """
    result = session.query(Courses).filter(Courses.name == name).all()
    if result:
        return True
    else:
        return False
