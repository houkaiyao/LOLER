from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'user_secret_key'
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ScamID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50), unique=True, nullable=False)
    first_reported = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    messages = get_flashed_messages()
    result = messages[0] if messages else None
    return render_template('index.html', result=result)

@app.route('/search', methods=['POST'])
def search():
    identifier = request.form.get('identifier', '').strip()
    result = ScamID.query.filter_by(identifier=identifier).first()

    if result:
        msg = f"该账号 {identifier}已被标记，首次记录时间：{result.first_reported.strftime('%Y-%m-%d')}"
    else:
        msg = f"该账号 {identifier} 尚未被标记。"




    flash(msg)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)