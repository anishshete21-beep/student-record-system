from database import execute_query, fetch_all, fetch_one


def add_student(roll, name, age, course):
    query = """
        INSERT INTO students (roll, name, age, course)
        VALUES (?, ?, ?, ?)
    """

    return execute_query(
        query,
        (roll, name, age, course)
    )


def get_all_students():
    query = """
        SELECT *
        FROM students
        ORDER BY id DESC
    """

    return fetch_all(query)


def get_student(student_id):
    query = """
        SELECT *
        FROM students
        WHERE id = ?
    """

    return fetch_one(
        query,
        (student_id,)
    )


def search_students(keyword):
    keyword = f"%{keyword}%"

    query = """
        SELECT *
        FROM students
        WHERE
            roll LIKE ?
            OR name LIKE ?
            OR course LIKE ?
        ORDER BY id DESC
    """

    return fetch_all(
        query,
        (keyword, keyword, keyword)
    )


def update_student(student_id, roll, name, age, course):
    query = """
        UPDATE students
        SET
            roll = ?,
            name = ?,
            age = ?,
            course = ?
        WHERE id = ?
    """

    execute_query(
        query,
        (
            roll,
            name,
            age,
            course,
            student_id
        )
    )


def delete_student(student_id):
    query = """
        DELETE FROM students
        WHERE id = ?
    """

    execute_query(
        query,
        (student_id,)
    )