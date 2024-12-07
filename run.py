from factory import create_app
from blueprints.auth import auth_bp

app = create_app()

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
