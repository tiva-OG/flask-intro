from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, timezone


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


class Todo(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  content: Mapped[str] = mapped_column(String(200), nullable=False)
  # completed: Mapped[int] = mapped_column(default=0)
  date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
  
  def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    task_content = request.form['content']
    new_task = Todo(content=task_content)
    
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue adding your task'
    
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)
  
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was an issue deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  task_to_update = Todo.query.get_or_404(id)
  
  if request.method == 'POST':
    task_to_update.content = request.form['content']
    
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating that task'
      
  else:
    return render_template('update.html', task=task_to_update)
  

"""
def create_test_db():
  with app.app_context():
    db.create_all()

"""
if __name__ == "__main__":
  app.run(debug=True)