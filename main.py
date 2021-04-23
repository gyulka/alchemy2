import requests
import api
from db import db_unit
from db.db_unit import User
from templates.forms.forms import LoginForm, RegisterForm, NewJob, EditJob, NewDep, EditDep
from flask import Flask, request, render_template, session, redirect, Blueprint , jsonify
from flask_login import LoginManager, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(db_unit.User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout', methods=['POST', "GET"])
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           jobs_now=db_sess.query(db_unit.Job).filter(db_unit.Job.is_finished == False).all(),
                           jobs_done=db_sess.query(db_unit.Job).filter(db_unit.Job.is_finished == True).all())


@app.route('/new_job', methods=['POST', 'GET'])
def new_job():
    form = NewJob()
    if form.validate_on_submit():
        job = db_unit.Job()
        job.is_finished = form.is_finished.data
        job.description = form.description.data
        job.team_leader = form.team_leader.data
        job.id_created = current_user.id
        job.hazard = form.hazard.data
        db_sess.add(job)
        db_sess.commit()

        return redirect('/')

    return render_template('new_job.html', form=form)


@app.route('/edit_job', methods=['POST', 'GET'])
def edit_job():
    form = EditJob()
    if form.validate_on_submit():
        job = db_sess.query(db_unit.Job).filter(db_unit.Job.id == int(request.args['id'])).first()
        job.is_finished = form.is_finished.data
        job.description = form.description.data
        job.team_leader = form.team_leader.data
        job.hazard = form.hazard.data
        db_sess.commit()

        return redirect('/')

    job = db_sess.query(db_unit.Job).filter(db_unit.Job.id == int(request.args['id'])).first()
    form.description.data = job.description
    form.team_leader.data = job.team_leader
    form.team.data = job.team
    form.hazard.data = job.hazard
    return render_template('new_job.html', form=form)


@app.route('/delete_job')
def delete_job():
    job = db_sess.query(db_unit.Job).filter(db_unit.Job.id == int(request.args['id'])).first()
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = NewDep()
    if form.validate_on_submit():
        dep = db_unit.Department()
        dep.members = form.team.data
        dep.email = form.email.data
        dep.chief = form.chief.data
        dep.title = form.title.data
        db_sess.add(dep)
        db_sess.commit()

        return redirect('/departments')

    return render_template('new_department.html', form=form)


@app.route('/edit_department', methods=['GET', 'POST'])
def edit_department():
    form = EditDep()
    if form.validate_on_submit():
        dep = db_sess.query(db_unit.Department).filter(db_unit.Department.id == int(request.args['id'])).first()
        dep.members = form.team.data
        dep.email = form.email.data
        dep.chief = form.chief.data
        dep.title = form.title.data
        db_sess.add(dep)
        db_sess.commit()

        return redirect('/')
    dep = db_sess.query(db_unit.Department).filter(db_unit.Department.id == int(request.args['id'])).first()
    form.team.data = dep.members
    form.email.data = dep.email
    form.chief.data = dep.chief
    form.title.data = dep.title

    return render_template('new_department.html', form=form)


@app.route('/delete_department', methods=['POST', 'GET'])
def delete_dep():
    dep = db_sess.query(db_unit.Department).filter(db_unit.Department.id == int(request.args['id'])).first()
    db_sess.delete(dep)
    db_sess.commit()
    return redirect('/departments')


@app.route('/departments', methods=['POST', 'GET'])
def index_dep():
    return render_template('departments.html', departments=db_sess.query(db_unit.Department).all())


@app.route('/users_show/<int:user_id>')
def index_users(user_id):
    city = requests.get(f'http://127.0.0.1:5000/api/user/{user_id}').json()
    if city['response']['success']:
        return render_template('city_form.html',
                               img=f"https://static-maps.yandex.ru/1.x/?l=sat,skl&spn=0.01,0.01&ll={city['response']['response']['city']}")
    else:
        return jsonify(response = {
            'success':False
        })


if __name__ == '__main__':
    db_unit.global_init("db/blogs.db")
    db_sess = db_unit.create_session()
    app.register_blueprint(api.blueprintJobs)
    app.register_blueprint(api.blueprintUser)
    app.run()
