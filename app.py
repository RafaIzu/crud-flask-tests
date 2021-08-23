from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import redirect

app = Flask(__name__)
db_url = 'localhost:5432'
db_name = 'delivery'
db_user = 'postgres'
db_password = 'toalha28'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///delivery.sqlite3'



db = SQLAlchemy(app)
class Consumer(db.Model):
    __tablename__ = 'consumer'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def index():
    consumer = Consumer.query.all()
    print(consumer) 
    return render_template('index.html', consumers=consumer)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['email'])
        consumer = Consumer(request.form['name'], request.form['email'])
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        print(">>",request.form['name'])
        print(">>",request.form['email'])
        db.session.commit()
        print('comitou')
        return redirect(url_for('index'))
    return render_template('edit.html', consumer=consumer)

@app.route('/delete/<int:id>')
def delete(id):
    consumer = Consumer.query.get(id)
    db.session.delete(consumer)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)