from flask import Flask, request, render_template
from db.connection import DatabaseConnection
from services.user_service import UserService

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dni = request.form.get('dni')
        if dni:
            user_service = UserService()
            user_service.add_user(dni)
            return render_template('index.html', message="Usuario agregado exitosamente.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)