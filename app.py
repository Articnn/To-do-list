from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task  # Importa la instancia db y el modelo User

''''
Flask es el framwork que se uso
SWLAlchemy interacuar base de datos
flask login maneja la autenticacion del usuario
werkzeug hash de contraseñas
models importa la instacia db y el modelo User 


'''




app = Flask(__name__)

# Configuraciones
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto por una clave secreta real
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa la instancia de SQLAlchemy con la aplicación

''''
SECRET_KEY: Clave secreta para sesiones y protección de formularios.
SQLALCHEMY_DATABASE_URI: Configura SQLite como la base de datos.
SQLALCHEMY_TRACK_MODIFICATIONS: Desactiva el seguimiento de modificaciones de objetos.


'''

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Carga el usuario con Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

''''
Login manager configura la configuracion de sesiones del usuario
user loader carga el usuario de la db usando id del usuario 


'''

# Rutas
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta 'templates'

''''
renderiza la pagina principal


'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tasks')) # en esta parte es donde se puede mandar al usuario una vez inicie sesion antes decia home recuerda es el nombre de la funcion
        else:
            flash('Invalid credentials')
    return render_template('login.html')

''''
maneja la autenticacion del usuario si el POST es valido redirige a dashboard si no muesta el mensaje de error


'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Usa 'pbkdf2:sha256'
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

''''
permite registrar nuevos usuarios la contraseña se guarda como un hash


'''

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}!'
    #return f'Hello', redirect(url_for('index'))

''''
muestra mensahe de bienvenida al usuario 


'''

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

''''
cierra la sesion del usuario y manda al login
para poder salir correctamente es necesario decirle que metodo 
usa en este caso es POST 

'''

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        new_task = Task(title=title, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/<int:task_id>/complete')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id) # se recupera la tarea 
    db.session.delete(task) # pa fuera 
    db.session.commit()
    return redirect(url_for('tasks'))

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()
    print("Database tables created")
    
''''
se supone que crea mas bien obliga la creacion de las tablas pero no funciono
fue manual con DB browser SQLite 


'''




if __name__ == "__main__":
    app.run(debug=True)
    
    
''''
Inicia la app en modo depuracion 


'''

