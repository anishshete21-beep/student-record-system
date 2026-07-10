"""
Test suite for the Student Record System.

Run with:
    python test_app.py

Uses a separate test database (test_database/test_students.db) so your
real students.db is never touched. The test database is deleted after
each test runs.
"""

import json
import os
import unittest

import database
import models
import api


TEST_DB_FOLDER = "test_database"
TEST_DB_FILE = "test_students.db"
TEST_DB_PATH = os.path.join(TEST_DB_FOLDER, TEST_DB_FILE)


class StudentSystemTests(unittest.TestCase):

    def setUp(self):
        # Point the app at a throwaway test database instead of the real one
        os.makedirs(TEST_DB_FOLDER, exist_ok=True)
        database.DATABASE_PATH = TEST_DB_PATH
        database.create_database()

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    # ---------- add ----------

    def test_add_student_success(self):
        result = json.loads(api.add({
            "roll": "1",
            "name": "Anish",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertTrue(result["success"])

    def test_add_student_missing_fields(self):
        result = json.loads(api.add({
            "roll": "1",
            "name": "",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Please fill all fields.")

    def test_add_student_duplicate_roll(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})

        result = json.loads(api.add({
            "roll": "1",
            "name": "Someone Else",
            "age": 22,
            "course": "Civil"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Roll number already exists.")

    def test_add_student_roll_too_low(self):
        result = json.loads(api.add({
            "roll": "0",
            "name": "Anish",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Roll number must be between 1 and 100.")

    def test_add_student_roll_too_high(self):
        result = json.loads(api.add({
            "roll": "101",
            "name": "Anish",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Roll number must be between 1 and 100.")

    def test_add_student_roll_not_a_number(self):
        result = json.loads(api.add({
            "roll": "abc",
            "name": "Anish",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Roll number must be between 1 and 100.")

    def test_add_student_roll_boundaries_allowed(self):
        low = json.loads(api.add({"roll": "1", "name": "A", "age": 20, "course": "Civil"}))
        high = json.loads(api.add({"roll": "100", "name": "B", "age": 20, "course": "Civil"}))

        self.assertTrue(low["success"])
        self.assertTrue(high["success"])

    def test_roll_number_reusable_after_delete(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        student_id = models.get_all_students()[0]["id"]

        api.remove(student_id)

        result = json.loads(api.add({
            "roll": "1",
            "name": "New Student",
            "age": 20,
            "course": "Civil"
        }))

        self.assertTrue(result["success"])

    # ---------- get all ----------

    def test_get_all_students_empty(self):
        result = json.loads(api.get_students())

        self.assertTrue(result["success"])
        self.assertEqual(result["students"], [])

    def test_get_all_students_after_add(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        api.add({"roll": "2", "name": "Priya", "age": 22, "course": "Electrical"})

        result = json.loads(api.get_students())

        self.assertTrue(result["success"])
        self.assertEqual(len(result["students"]), 2)

    # ---------- get single ----------

    def test_get_single_student_found(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        student_id = models.get_all_students()[0]["id"]

        result = json.loads(api.get_single_student(student_id))

        self.assertTrue(result["success"])
        self.assertEqual(result["student"]["name"], "Anish")

    def test_get_single_student_not_found(self):
        result = json.loads(api.get_single_student(999))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Student not found.")

    # ---------- update ----------

    def test_update_student_success(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        student_id = models.get_all_students()[0]["id"]

        result = json.loads(api.update(student_id, {
            "roll": "1",
            "name": "Anish Updated",
            "age": 22,
            "course": "Civil"
        }))

        self.assertTrue(result["success"])

        updated = models.get_student(student_id)
        self.assertEqual(updated["name"], "Anish Updated")
        self.assertEqual(updated["course"], "Civil")

    def test_update_student_not_found(self):
        result = json.loads(api.update(999, {
            "roll": "1",
            "name": "Anish",
            "age": 21,
            "course": "Computer Science"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Student not found.")

    def test_update_student_duplicate_roll(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        api.add({"roll": "2", "name": "Priya", "age": 22, "course": "Electrical"})

        priya_id = [s for s in models.get_all_students() if s["roll"] == "2"][0]["id"]

        result = json.loads(api.update(priya_id, {
            "roll": "1",
            "name": "Priya",
            "age": 22,
            "course": "Electrical"
        }))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Roll number already exists.")

    # ---------- delete ----------

    def test_delete_student_success(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        student_id = models.get_all_students()[0]["id"]

        result = json.loads(api.remove(student_id))

        self.assertTrue(result["success"])
        self.assertIsNone(models.get_student(student_id))

    def test_delete_student_not_found(self):
        result = json.loads(api.remove(999))

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Student not found.")

    # ---------- search ----------

    def test_search_by_name(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})
        api.add({"roll": "2", "name": "Priya", "age": 22, "course": "Electrical"})

        result = json.loads(api.search("Anish"))

        self.assertTrue(result["success"])
        self.assertEqual(len(result["students"]), 1)
        self.assertEqual(result["students"][0]["name"], "Anish")

    def test_search_by_roll(self):
        api.add({"roll": "42", "name": "Anish", "age": 21, "course": "Computer Science"})

        result = json.loads(api.search("42"))

        self.assertEqual(len(result["students"]), 1)

    def test_search_by_course(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Mechanical"})
        api.add({"roll": "2", "name": "Priya", "age": 22, "course": "Electrical"})

        result = json.loads(api.search("Mechanical"))

        self.assertEqual(len(result["students"]), 1)
        self.assertEqual(result["students"][0]["name"], "Anish")

    def test_search_no_match(self):
        api.add({"roll": "1", "name": "Anish", "age": 21, "course": "Computer Science"})

        result = json.loads(api.search("Nonexistent"))

        self.assertTrue(result["success"])
        self.assertEqual(result["students"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)