import os
import os.path as op
import tempfile
import json
import pytest
from flask import url_for

from app.models.treasure_item import TreasureItem
from app.models.student import Student
from app.models.transaction import Transaction

from app.model_views.transaction import reject_transactions, approve_transactions

student_mock_data = []
treasure_item_mock_data = []

with open(op.join(op.dirname(__file__), 'mocks', 'ten_students.json'), "r") as read_file:
    student_mock_data = json.load(read_file)

with open(op.join(op.dirname(__file__), 'mocks', 'ten_treasure_items.json'), "r") as read_file:
    treasure_item_mock_data = json.load(read_file)


def create_transactions(db, txns):
    txn_ids = []
    for txn in txns:
        transaction = Transaction(
            active=True,
            student_id=txn['student_id'],
            treasure_item_id=txn['treasure_item_id'])
        db.session.add(transaction)
        db.session.commit()
        txn_ids.append(transaction.id)

    return txn_ids


def create_students(db, students):
    for student in students:
        student = Student(
            first_name=student['first_name'],
            last_name=student['last_name'],
            passcode=student['passcode'],
            active=True,
            points=student['points'])
        db.session.add(student)

    db.session.commit()


def create_treasure_item(db, treasure_items):
    for treasure_item in treasure_items:
        treasureItem = TreasureItem(
            cost=treasure_item['cost'],
            name=treasure_item['name'],
            description='It\'s a cool item',
            quantity=treasure_item['quantity'])
        db.session.add(treasureItem)

    db.session.commit()


class TestApprovals:
    def test_reject_single(self, db):
        create_students(db, student_mock_data)
        create_treasure_item(db, treasure_item_mock_data)

        txn_ids = create_transactions(db, [{
            "student_id": 1,
            "treasure_item_id": 1
        }, {
            "student_id": 2,
            "treasure_item_id": 1
        }])

        reject_transactions(txn_ids)
        item_count = TreasureItem.query.get(1).quantity
        student_one_points = Student.query.get(1).points
        student_two_points = Student.query.get(2).points
        active = Transaction.query.filter_by(active=True).count()
        assert (item_count, student_one_points,
                student_two_points, active) == (74, 80, 24, 0)

    def test_approval(self):
        pass
        # create_students(treasure_item_mock_data)
