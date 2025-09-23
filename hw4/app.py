'''
Добавить к прошлому проекту 2 страницы 
    - страницу с формой регистрации.
        Регистрация должна содержать имя фамилию возраст email логин пароль.
        После отправки формы регистрации проверить данные на валидность
            - имя фамилия - только русские буквы
            - логин - латинские цифры и _. От 6 до 20 символов
            - пароль - обязательно хотя бы 1 латинская маленькая, 1 заглавная и  1 цифр. От 8 до 15 символов.
            - * email - должен быть валидным
            - * возраст - целое число от 12 до 100
        При успешной проверке  добавить пользователя в базу/файл/список/словарь 
            и направить пользователя на форму входа.
        При выявлении ошибок снова показать форму, но уже с заполненными полями 
            и в любом месте формы показать список ошибок.
        
    - страницу с формой входа на сайт.
        - при успешном входе                             
            - пометить в сессиях что он залогинился
            - перенаправить на главную страницу
        - при ошибке показать форму снова, с сообщением об ошибке



Все прежние страницы сделать открытыми только для пользователей которые произвели вход на сайт.
Если пользователь не залогинился и переходит на них - перенаправлять его на форму входа. 
На фоме входа сделать ссылку на форму регистрации.

Если пользовался залогинился - на каждой странице сверху писать - "Приветствуем вас имя фамилия"

На главной странице показывать ссылку ВХОД и РЕГИСТРАЦИЯ для пользователей которые не вошли на сайт
и ссылку ВЫХОД для  пользователей которые вошли на сайт

Таким образом новый пользователь имеет доступ  только на главную страницу где есть ссылка на вход регистрацию.
После регистрации и входа он имеет доступ на все доступные страницы.

'''

from flask import Flask, render_template, redirect, request, url_for, session
import weather
import session_model

app = Flask(__name__)

app.secret_key = "123_надо _использовать_генератор?"

@app.context_processor
def inject_login():
    login_menu = "Войти"
    login_url = "/login"
    user = None
    if session_model.is_login() == True:
        user = session_model.current_user()
        login_menu = f"Выйти ({user["fname"]})"
        login_url = "/logout"

    return {
        "login_menu": login_menu,
        "login_url": login_url,
        "user": user
    } 

@app.route("/")
def index():
    # if session_model.is_login() == False:
        # return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def login_page():
    err = ""
    if request.method == "POST":
        res, err = session_model.check_login(request.form)
        if  res == True:
            return redirect(url_for('index'))
    return render_template('login.html', errors = err)

@app.route("/signup/", methods=['GET', 'POST'])
def sigup_page():
    err = None
    data = None
    if request.method == "POST":
        res, err = session_model.check_reg(request.form)
        if  res == True:
            return redirect(url_for('index'))
        else:
            data = request.form
    return render_template('signup.html', errors = err, data = data)

@app.route("/logout/")
def logout():
    session_model.logout()
    return redirect(url_for('login_page'))

@app.route("/weather/")
def weather_page():
    if session_model.is_login() == False:
        return redirect(url_for('login_page'))
    return render_template('weather.html')

@app.route("/weather/<city>")
def weather_city(city):
    if session_model.is_login() == False:
        return redirect(url_for('login_page'))
    city_weather = weather.city(city)
    return render_template('city.html', data = city_weather)

# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found():
    return render_template('error404.html')

app.run(debug=True)