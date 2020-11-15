def register(app):
    @app.route('/')
    def main():
        return 'Main page'

    @app.route('/admin')
    def adminLogin():
        return 'Admin login'

    @app.route('/helloworld')
    def hello_world():
        return 'Hello, World!'
