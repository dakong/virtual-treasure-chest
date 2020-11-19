from sqlalchemy.orm import join
from app.model_views.model_view_base import ModelViewAuth
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin.actions import action
from app import db
from app.models.treasure_item import TreasureItem
from app.models.student import Student
from app.models.transaction import Transaction


def reject_transactions(ids):
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

    # Set all transactions proccessed to false
    Transaction.query.filter(
        Transaction.id.in_(ids)).update({'active': False}, synchronize_session='fetch')

    db.session.commit()


def approve_transactions(ids):
    Transaction.query.filter(
        Transaction.id.in_(ids)).update({'active': False}, synchronize_session='fetch')
    db.session.commit()


class TransactionView(ModelViewAuth):
    def get_query(self):
        return super(TransactionView, self).get_query().filter(Transaction.active == True)

    def get_count_query(self):
        return super(TransactionView, self).get_count_query().filter(Transaction.active == True)

    @action('approve', 'Approve', 'Are you sure you want to approve selected transactions?')
    def action_approve(self, ids):
        approve_transactions(ids)

    @action('reject', 'Reject', 'Are you sure you want to reject selected transactions?')
    def action_reject(self, ids):
        reject_transactions(ids)

    can_delete = False
    export_types = ['csv', 'xlsx']
    column_exclude_list = ('active',)
    list_template = 'transaction_list.html'
