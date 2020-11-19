from flask import session
from sqlalchemy.orm import join
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin.actions import action
from app import db
from app.model.treasure_item import TreasureItem
from app.model.student import Student
from app.model.transaction import Transaction


class TransactionView(ModelView):
    def is_accessible(self):
        return 'userID' in session

    def get_query(self):
        return super(TransactionView, self).get_query().filter(Transaction.active == True)

    def get_count_query(self):
        return super(TransactionView, self).get_count_query().filter(Transaction.active == True)

    @action('approve', 'Approve', 'Are you sure you want to approve selected transactions?')
    def action_approve(self, ids):
        Transaction.query.filter(
            Transaction.id.in_(ids)).update({'active': False}, synchronize_session='fetch')
        db.session.commit()

    @action('reject', 'Reject', 'Are you sure you want to reject selected transactions?')
    def action_reject(self, ids):
        transactions = Transaction.\
            query.join(Transaction.student).\
            join(Transaction.treasure_item).\
            filter(db.and_(Transaction.id.in_(ids), Transaction.active == True)).\
            all()

        # Create dict of studentID to reimbursment costs
        reimbursement = {}
        # Create dict of treasureItemID count
        restock = {}

        for txn in transactions:
            if txn.student.id in reimbursement:
                reimbursement[txn.student_id] += txn.treasure_item.cost
            else:
                reimbursement[txn.student_id] = txn.treasure_item.cost

            if txn.treasure_item_id in restock:
                restock[txn.treasure_item_id] += 1
            else:
                restock[txn.treasure_item_id] = 1

        # stock back quantity of the item
        for treasure_item_id in restock:
            treasure_item = TreasureItem.query.get(treasure_item_id)
            treasure_item.quantity += restock[treasure_item_id]

        # Refund student's points
        for student_id in reimbursement:
            student = Student.query.get(student_id)
            student.points += reimbursement[student_id]

        db.session.commit()

    can_delete = False
    export_types = ['csv', 'xlsx']
    column_exclude_list = ('active',)
    list_template = 'transaction_list.html'
