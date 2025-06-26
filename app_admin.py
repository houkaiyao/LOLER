from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# 设置数据库路径
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据模型
class ScamID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50), unique=True, nullable=False)
    first_reported = db.Column(db.DateTime, default=datetime.utcnow)

# 管理页面
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

# 标记 / 删除操作
@app.route('/admin/operate', methods=['POST'])
def operate():
    identifier = request.form.get('identifier', '').strip()
    action = request.form.get('action')

    if not identifier:
        return redirect(url_for('admin'))

    if action == 'mark':
        existing = ScamID.query.filter_by(identifier=identifier).first()
        if not existing:
            new_entry = ScamID(identifier=identifier)
            db.session.add(new_entry)
            db.session.commit()
    elif action == 'delete':
        existing = ScamID.query.filter_by(identifier=identifier).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
