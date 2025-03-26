from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLiteデータベースの設定
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 初期化
init_db()

# タスクの表示
@app.route('/')
def index():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM todos')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# タスクの追加
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        c.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# タスクの削除
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
