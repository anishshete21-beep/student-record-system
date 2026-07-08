import json
import sqlite3

from models import (
    add_student,
    get_all_students,
    get_student,
    search_students,
    update_student,
    delete_student
)


def get_students():
    try:
        students = get_all_students()

        return json.dumps({
            "success": True,
            "students": students
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })


def get_single_student(student_id):
    try:
        student = get_student(student_id)

        if student is None:
            return json.dumps({
                "success": False,
                "message": "Student not found."
            })

        return json.dumps({
            "success": True,
            "student": student
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })


def search(keyword):
    try:
        students = search_students(keyword)

        return json.dumps({
            "success": True,
            "students": students
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })


def add(data):
    try:

        roll = data.get("roll", "").strip()
        name = data.get("name", "").strip()
        age = data.get("age")
        course = data.get("course", "").strip()

        if not roll or not name or not age or not course:
            return json.dumps({
                "success": False,
                "message": "Please fill all fields."
            })

        add_student(
            roll,
            name,
            int(age),
            course
        )

        return json.dumps({
            "success": True,
            "message": "Student added successfully."
        })

    except sqlite3.IntegrityError:
        print("Duplicate Roll Number")

        return json.dumps({
            "success": False,
            "message": "Roll number already exists."
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })


def update(student_id, data):
    try:

        student = get_student(student_id)

        if student is None:
            return json.dumps({
                "success": False,
                "message": "Student not found."
            })

        roll = data.get("roll", "").strip()
        name = data.get("name", "").strip()
        age = data.get("age")
        course = data.get("course", "").strip()

        if not roll or not name or not age or not course:
            return json.dumps({
                "success": False,
                "message": "Please fill all fields."
            })

        update_student(
            student_id,
            roll,
            name,
            int(age),
            course
        )

        return json.dumps({
            "success": True,
            "message": "Student updated successfully."
        })

    except sqlite3.IntegrityError:
        print("Duplicate Roll Number")

        return json.dumps({
            "success": False,
            "message": "Roll number already exists."
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })


def remove(student_id):
    try:

        student = get_student(student_id)

        if student is None:
            return json.dumps({
                "success": False,
                "message": "Student not found."
            })

        delete_student(student_id)

        return json.dumps({
            "success": True,
            "message": "Student deleted successfully."
        })

    except Exception as e:
        print(e)

        return json.dumps({
            "success": False,
            "message": str(e)
        })