import os
import tempfile
import pytest
from flask import url_for


def register_teacher(testapp, **kwargs):
    return testapp.post_json('/api/teacher/', {
        'first_name': 'admin',
        'last_name': 'example',
        'username': 'admin.example',
        'password': 'admin'
    }, **kwargs)


def login(testapp, *args, **kwargs):
    return testapp.post('/login/', {
        'username': args[0],
        'password': args[1]
    }, **kwargs)


class TestAuthentication:
    def test_admin_404(self, testapp):
        resp = testapp.get('/admin/', expect_errors=True)
        assert resp.status_int == 404

    def test_student_404(self, testapp):
        resp = testapp.get('/admin/student/', expect_errors=True)
        assert resp.status_int == 404

    def test_transaction_404(self, testapp):
        resp = testapp.get('/admin/transaction/', expect_errors=True)
        assert resp.status_int == 404

    def test_treasure_item_404(self, testapp):
        resp = testapp.get('/admin/treasureitem/', expect_errors=True)
        assert resp.status_int == 404

    def test_login(self, testapp):
        teacher = register_teacher(testapp)
        resp = login(testapp, 'admin.example', 'admin').follow()
        assert resp.status_int == 200 and resp.request.path == '/admin/'

    def test_student_200(self, testapp):
        teacher = register_teacher(testapp)
        resp = testapp.post(url_for("login"), {
            'username': 'admin.example',
            'password': 'admin'
        })
        resp = testapp.get('/admin/student/', expect_errors=True)
        assert resp.status_int == 200

    def test_transaction_200(self, testapp):
        teacher = register_teacher(testapp)

        resp = testapp.post(url_for("login"), {
            'username': 'admin.example',
            'password': 'admin'
        })
        resp = testapp.get('/admin/transaction/', expect_errors=True)
        assert resp.status_int == 200

    def test_treasure_item_200(self, testapp):
        teacher = register_teacher(testapp)

        resp = testapp.post(url_for("login"), {
            'username': 'admin.example',
            'password': 'admin'
        })
        resp = testapp.get('/admin/treasureitem/', expect_errors=True)
        assert resp.status_int == 200
