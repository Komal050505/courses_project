from course_model.table import Courses
from course_db_connections.configurations import session

# FLASK BACKEND
from flask import Flask, request, jsonify
from flask_restful import Api

from courses_app.db_operations import is_course_exist
from course_utils.reusables  import *

# CREATE BACKEND APP
app = Flask(__name__)


@app.route('/create-course', methods=['POST'])
def create_course():
    # Collect the course information from the client device
    user_data = request.get_json()
    print(f"User data is : {user_data}")

    if not is_course_exist(user_data['name']):
        try:
            record = Courses(name=user_data.get('name'),
                             fee=user_data.get('fee'),
                             part_time=user_data.get('partTime'),
                             full_time=user_data.get('fullTime'),
                             weeks=user_data.get('weeks'),
                             online=user_data.get('inPerson'),
                             inperson=user_data.get('online'))
            session.add(record)
            session.commit()
            return success_response(f"{user_data['name']} created successfully")
        except Exception as err:
            print(f"Error occurred is - {err}")
            # If error occurs current database operation should be roll back crud operations to previous state
            session.rollback()
            return failure_response(f"Database operation failed reason -{err}")
    else:
        return failure_response(f"Course {user_data['name']} already exist please create different course")


@app.route('/course-details', methods=['GET'])
def fetch_courses():
    try:
        result = session.query(Courses).all()
    except Exception as err:
        print(f"Error occurred is ---{err}")
    results_dict = [item.__dict__ for item in result]
    print(f"Result : {result}")
    print(f"Result to Dict : {results_dict}")
    for item in results_dict:
        # Remove _sa_instance_state form the list of dicts
        del item['_sa_instance_state']
    print(f"Cleaned Dict - {results_dict}")
    if results_dict:
        return success_response(results_dict)
    else:
        return failure_response(f"production_id {results_dict} doesnot exist")






@app.route('/single-course', methods=['GET'])
def single_courses():
    result = []
    user_course_selection = request.args.get('name')
    try:
        result = session.query(Courses).filter(Courses.name == user_course_selection).all()
    except Exception as err:
        print(f"Error occurred is {err}")
    results_dict = [item.__dict__ for item in result]
    print(f"Result : {result}")
    print(f"Result to Dict : {results_dict}")
    for item in results_dict:
        # Remove _sa_instance_state form the list of dicts
        del item['_sa_instance_state']
    print(f"Cleaned Dict - {results_dict}")
    if results_dict:
        return success_response(results_dict)
    else:
        return failure_response(f"Course name {user_course_selection} doesn't exist")


# This is not a standard way for PATCH method
# Updating few columns with values using request parameters
@app.route('/update-course', methods=['PATCH'])
def updated_courses():
    """
    This function update the course table
    """

    # Takes the user parameters from the keyboard
    user_course_selection = request.args.get('name')
    if not is_course_exist(request.args.get('name')):
        return failure_response(f"Course {request.args.get('name')} doesn't exist")
    updated_fee = request.args.get('fee')

    try:
        session.query(Courses).filter(Courses.name == user_course_selection).update({"fee": updated_fee})
        session.commit()
        return success_response(f"{user_course_selection} course has been updated with {updated_fee}")
    except Exception as err:
        session.rollback()
        return failure_response(f"Database update operation failed reason -{err}")


# Recommended to use request body in the enterprise application development
# Updating many columns with values using request body/payload
@app.route('/update-course-table', methods=['PATCH'])
def updated_course_table():
    data = request.get_json()
    print(f"Data is : {data}")
    session.query(Courses).filter(Courses.name == data['name']).update(data)
    session.commit()
    return f"{data['name']} course has been updated with {data['fee']}"


# Recommanded Way
@app.route('/delete-course', methods=['DELETE'])
def delete_course_table():
    data = request.get_json()
    print(f"Data is : {data}")
    if not session.query(Courses).filter(Courses.name == data['name']).all():
        return f"{data['name']} course doesn't exist"
    session.query(Courses).filter(Courses.name == data['name']).delete()
    session.commit()
    return f"{data['name']} course has been deleted"


@app.route('/delete-courses', methods=['DELETE'])
def delete_courses():

    # Inputs receiving
    data = request.get_json()
    print(f"Data is : {data}")

    # Validating some stuff
    if not is_course_exist(data['name']):
        return failure_response("{data['name']} course doesn't exist")

    # Doing actual work
    try:
        session.query(Courses).filter(Courses.name == data['name']).delete()
        session.commit()
        # Returning the response
        return success_response(f"{data['name']} course has been deleted")
    except Exception as err:
        session.rollback()
        return failure_response(f"Unable to delete course {data['name']}")


app.run()
