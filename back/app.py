from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'thejayadad'

conn = psycopg2.connect(host="localhost", dbname="notes", user="postgres", password="football", port=5432)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS note(
    id INT PRIMARY KEY,
    title VARCHAR(55),
    content VARCHAR(255)
)
            """)

# insert_scripts = 'INSERT INTO note (id, title, content) VALUES (%s,%s,%s)'
# insert_value = (10, "Exercise", "Get 45 minutes of exercise")

# cur.execute(insert_scripts, insert_value)

#GET ALL
@app.route("/", methods=['GET'])
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    n = "SELECT * FROM note"
    cur.execute(n)
    list_notes = cur.fetchall()
    return render_template("index.html", list_notes = list_notes)


#ADD NOTE ROUTE
@app.route("/add_note", methods=['POST'])
def add_note():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        cur.execute("INSERT INTO note (id, title, content) VALUES (%s,%s,%s)", (id, title, content))
        conn.commit()
        return redirect(url_for('Index'))

#EDIT ROUTE
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_note(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM note WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', note = data[0])

#UPDATE POST ROUTE
@app.route('/update/<id>', methods=['POST'])
def update_note(id):
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE note
            SET id = %s,
                title = %s,
                content = %s
            WHERE id = %s
        """, (id, title, content, id))
        conn.commit()
        return redirect(url_for('Index'))

#DELETE ROUTE
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_note(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM note WHERE id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('Index'))


conn.commit()


if __name__ == "__main__":
    app.run(debug=True)