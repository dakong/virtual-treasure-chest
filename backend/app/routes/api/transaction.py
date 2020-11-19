from flask import current_app as app, request, session, url_for, render_template, redirect
from app import db
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.model.transaction import Transaction


@ app.route('/api/transaction', methods=['POST'])
def transaction():
    transaction = request.get_json()

    transaction = Transaction(
        active=True,
        student_id=transaction['student_id'],
        treasure_item_id=transaction['treasure_item_id'])

    db.session.add(transaction)
    db.session.commit()

    return generateSuccessResponse({
        'transaction': {
            'id': transaction.id,
            'student_id': transaction.student_id,
            'treasure_item_id': transaction.treasure_item_id
        }
    })
