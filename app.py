from flask import Flask, render_template, request, redirect, url_for, flash
from database import select_query, execute_query
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    todos = select_query('SELECT id, title, complete FROM todos ORDER BY date_created DESC')
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    execute_query(query='INSERT INTO todos (title) VALUES (%s)', params=(title,))
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_todo(id):
    todo = select_query('SELECT complete FROM todos WHERE id = %s', (id,))
    if todo:
        new_status = not todo[0]['complete']
        execute_query('UPDATE todos SET complete = %s WHERE id = %s', (new_status, id,))
        
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    execute_query(query='DELETE FROM todos WHERE id = %s', params=(id,))
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)