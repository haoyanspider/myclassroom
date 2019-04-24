from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
import config
from decorators import login_required
from models import User, Question, Answer
from werkzeug.routing import BaseConverter
import datetime
import time


class Tel(BaseConverter):
    regex = r'(13|14|15|17|18)[0-9]{9}'


app = Flask(__name__)
app.config.from_object(config)
app.url_map.converters['Tel'] = Tel
db.init_app(app)


# 首页
@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('index.html', **context)


# 登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '用户名或者密码不正确！'


# 注册页面
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        # 手机号码验证
        if user:
            return '该手机号已被注册'
        else:
            if password1 != password2:
                return '两次密码不一样，请确认后重新注册！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


# 注销
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 发布问题
@app.route('/question')
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user = User.query.filter(User.id == session.get('user_id')).first()
        question = Question(title=title, content=content, author=user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


# 问题详情页面
@app.route('/detail/<question_id>/')
# @login_required
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    answer_count = Answer.query.filter(Answer.question_id == question.id).count()
    context = {
        'question': question,
        'answer_count': answer_count
    }
    return render_template('detail.html', **context)


# 发布评论
@app.route('/answer/', methods=['POST'])
def answer():
    content = request.form.get('answer')
    question_id = request.form.get('question_id')
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    print('hello', content, question_id)
    question = Question.query.filter(Question.id == question_id).first()
    answer = Answer(content=content, author=user, question=question)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


# 上下文处理器
@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return {'user': user}
    else:
        return {}
    # return {'name': 'huanghaoyan'}


if __name__ == '__main__':
    app.run()