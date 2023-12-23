
import time

import psycopg2
from flask import Flask, redirect, request, render_template,session,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
import pandas as pd
from flask import jsonify
from openpyxl import Workbook


SQLA_CONFIG_STR = f"postgresql://postgres:111@localhost:5432/MYOR"

app = Flask(__name__, template_folder='templates')

app.secret_key = 'your-secret-key'



def get_table_model(table_name):
    table_models = {
        'vehicle': Vehicle,
        'persons': persons,
        'ito': ito,
        'electro': Electro,
        'food': Food
    }
    return table_models.get(table_name)


def get_table_data(selected_table, count_limit):
    models = [Vehicle, persons, ito, Electro, Food]
    if selected_table not in [model.__tablename__ for model in models]:
        raise ValueError('Invalid request. Incorrect table name')

    selected_model = get_table_model(selected_table)
    if not selected_model:
        raise ValueError('Model not found for the given table name')

    # Визначення колонки для сортування
    if selected_table == 'vehicle':
        sort_column = Vehicle.number
    else:
        sort_column = selected_model.id

    table_data = selected_model.query.order_by(sort_column).limit(count_limit).all()
    column_names = [column.key for column in selected_model.__table__.columns]

    return column_names, table_data

@app.route('/')
def index():
    return render_template('login.html')



@app.route('/update_row', methods=['POST'])
def update_row():
    table_name = request.form.get('table_name')
    row_id = request.form.get('row_id')
    updated_data = {column: request.form.get(column) for column in request.form if
                    column != 'table_name' and column != 'row_id'}

    model_class = get_table_model(table_name)

    if model_class is None:
        return 'Table not found'

    row = model_class.query.get(row_id)

    if row is None:
        return 'Row not found'


    for column, value in updated_data.items():
        setattr(row, column, value)


    db.session.commit()
    selected_table = table_name
    limit = 10
    column_names, table_data = get_table_data(selected_table, limit)
    FIO = session.get('name', False)
    return render_template('site.html', column_names=column_names, table_data=table_data, table_name=selected_table,FIO=FIO)


@app.route('/add_row', methods=['GET'])
def add_row():
    FIO = session.get('name', False)
    return render_template('add_row.html',FIO=FIO)

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    conn = psycopg2.connect(database="MYOR", user="postgres", password="111", host="localhost",
                            port=5432)
    cur = conn.cursor()

    cur.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE login = '{login}')")
    result = cur.fetchone()[0]
    if result != True:
        return "Користувача з такою електронною поштою не існує"

    cur.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE password = '{password}')")
    result = cur.fetchone()[0]
    if result!= True:
        return "Невірний пароль"

    cur.execute(f"SELECT full_name FROM users WHERE login = '{login}'")
    name =cur.fetchone()[0]
    session['logged_in'] = True
    session['name'] = name
    session['login'] = login
    return redirect('/main')


def get_distinct_values_p(table_name, column_name):
    YourTableName = get_table_model(table_name)
    distinct_values = db.session.query(distinct(getattr(YourTableName, column_name)).label('count')).all()

    return distinct_values


@app.route('/add_rows', methods=['POST'])
def add_rows():
    table_name = request.form['table_name']
    updated_data = {column: request.form.get(column) for column in request.form if
                    column != 'table_name' and column != 'row_id'}
    model_class = get_table_model(table_name)
    row = model_class(**updated_data)
    db.session.add(row)
    db.session.commit()
    return redirect('/main')


@app.route('/upgate_row', methods=['POST'])
def upgate_row():
    table_name = request.form['table-select']
    column_names, table_data = get_table_data(table_name, 1)
    excluded_column = ['ID']

    for column in excluded_column:
        if column in column_names:
            column_names.remove(column)
    result = {}
    special_colum = []
    for i in column_names:
        temp = get_distinct_values_p(table_name, i)
        if len(temp) <= 2:
            result[i] = [temp]
            special_colum.append(i)
    FIO = session.get('name', False)
    return render_template('add_row.html', selected_table=table_name, columns=column_names, special_colum=special_colum,
                           result=result,FIO=FIO)


@app.route('/upgrade', methods=['POST'])
def upgrade():
    row_id = request.form['row_id']
    table_name = request.form['table_name']

    table_model = get_table_model(table_name)
    row = table_model.query.get(row_id)


    for column in row.__table__.columns:
        column_name = column.name
        new_value = request.form.get(column_name)
        setattr(row, column_name, new_value)


    db.session.commit()

    return render_template('edit_row.html', row=row, table_name=table_name, row_id=row_id)


@app.route('/delete_row', methods=['POST'])
def delete_row():
    row_id = request.form['row_id']
    table_name = request.form['table_name']

    table_model = get_table_model(table_name)
    row = table_model.query.get(row_id)

    db.session.delete(row)
    db.session.commit()

    return redirect('/main')


@app.route('/search', methods=['POST'])
def search():
    table_search = request.form['table_search']
    column_search = request.form['column_search']
    value_search = request.form['value_search']

    model_class = get_table_model(table_search)
    table_data = db.session.query(model_class).filter(getattr(model_class, column_search) == value_search).limit(
        20).all()

    column_names = [column.name for column in model_class.__table__.columns]
    FIO = session.get('name', False)
    return render_template('site.html', table_data=table_data, table_name=table_search, column_names=column_names,
                           search_data=[table_search, column_search, value_search], limit=10,FIO=FIO)


@app.route('/get_columns', methods=['POST'])
def get_columns():
    table = request.json['table']
    columns, _ = get_table_data(table, 1)

    return jsonify(columns)


@app.route('/main', methods=['GET', 'POST'])
def table(limit=10):
    if request.method == 'POST':
        selected_table = request.form['table']
        limit = int(request.form['limit'])
        column_names, table_data = get_table_data(selected_table, limit)
    else:
        column_names = None
        table_data = None
        selected_table = None
    FIO= session.get('name', False)
    return render_template('site.html', column_names=column_names,
                           table_data=table_data, table_name=selected_table, limit=limit,FIO=FIO)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/download_excel')
def download_excel():
    tables= ['vehicle','persons','ito','electro','food']
    # Підключення до бази даних
    conn = psycopg2.connect(database="MYOR", user="postgres", password="111", host="localhost",
                        port=5432)
    # Створення Excel-письменника
    excel_file = "Звіт.xlsx"
    writer = pd.ExcelWriter(excel_file, engine='openpyxl')
    for table in tables:
        # Вибірка даних з таблиці
        df = pd.read_sql(f"SELECT * FROM {table}", conn)

        # Запис даних у лист Excel
        df.to_excel(writer, sheet_name=table, index=False)

        # Правильне закриття та збереження файлу
    writer.close()
    # Закриття підключення до бази даних
    conn.close()
    # Відправка файлу користувачу
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLA_CONFIG_STR
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    from models import *

    db.init_app(app)

    start_time = time.time()

    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000
    )
    fin_time = time.time() - start_time