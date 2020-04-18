from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer, UserInfo, Notice, Garbage, ExtraInfo, News, Video
from extra import db
from decorators import login_required, manager_required
import random
import time, requests, re, datetime
import os, json


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
i = 1


@app.route('/')
def men():  # 入口
    return render_template('men.html')


@app.route('/home/', methods=['GET', 'POST'])  # 主页
def index():  # 主页
    if request.method == 'GET':
        content = {
            'questions': Question.query.order_by(Question.create_time.desc()).all()
        }
        if session.get('user_name') and '管理员' in session.get('user_name'):  # 管理员首页
            return render_template('manager.html', **content)
        else:  # 游客、用户首页
            return render_template('index.html', **content)
    else:
        if(request.form.get('id')):  # 删除问题
            question_id = request.form.get('id')
            question_1 = Question.query.filter(Question.id == question_id).first()
            db.session.delete(question_1)
            db.session.commit()
            content = {
                'questions': Question.query.order_by(Question.create_time.desc()).all()
            }
            return render_template('manager.html', **content)
        else:  # 搜索框
            search = request.form.get('search')
            garbage = Garbage.query.filter(Garbage.name == search).first()
            if(garbage):
                print(garbage)
                return render_template('garbage.html', garbage_model=garbage)
            question = Question.query.filter(Question.title.contains(search)).first()
            if(question):
                number_answer = len(question.answers)
                return render_template('detail.html', question_model=question, number_answer=number_answer)
            else:
                return 'no search'


@app.route('/test/', methods=['GET', 'POST'])  # 考试
@login_required
def test():
    global garbage
    if request.method == 'GET':
        garbage = Garbage.query.filter(Garbage.id == random.randint(1, 3000)).first()  # 随机出垃圾
        content = {
            'garbage': garbage  # 随机出垃圾
        }
        return render_template('test.html', **content)
    else:
        garbage_choice = request.form.get('garbage')  # 你选了啥
        user1 = User.query.filter(User.id == session.get('user_id')).first()
        print(session.get('user_name'))
        if (request.form.get('next')):  # 下一题
            garbage = Garbage.query.filter(Garbage.id == random.randint(1, 3000)).first()  # 随机出垃圾
            content = {
                'garbage': garbage  # 随机出垃圾
            }
        else:  # 选择选项
            if(garbage.code_id == int(garbage_choice)):  # 选对了加一分
                user1.score = session.get('score')+1
                session['score'] += 1
                answer = '答对了！ ' + garbage.name + '是' + str(garbage.code_name)
                print('答对了！ ' + garbage.name + '是' + str(garbage.code_name))
            else:  # 答错扣一分
                user1.score = session.get('score') - 1
                session['score'] -= 1
                answer = '答错了,'+garbage.name+'是'+str(garbage.code_name)
                print('答错了，'+garbage.name+'是'+str(garbage.code_name))
            db.session.commit()
            print(garbage.name)
            content = {
                'garbage': garbage,  # 随机出垃圾
                'answer': answer
            }
            return render_template('test.html', **content)
        return render_template('test.html', **content)


@app.route('/classroom/<int:page>')
def classroom(page=1):
    videos = Video.query.filter(Video.code_id == 2)
    video = videos.paginate(page, 15, False)
    return render_template('classroom.html', videos=video)


@app.route('/notice/', methods=['GET', 'POST'])  # 公告页面
@login_required
def notice():
    flag = 1
    if ('管理员' in session.get('user_name')):
        flag = 0
    content = {
        'flag': flag,
        'notices': Notice.query.filter(Notice.school == session.get('school')).order_by(
            Notice.create_time.desc()).all()
    }
    if request.method == 'POST':
        notice_id = request.form.get('notice_id')
        notice_1 = Notice.query.filter(Notice.id == notice_id).first()
        db.session.delete(notice_1)
        db.session.commit()
        print(notice_id)
        content = {
            'flag': flag,
            'notices': Notice.query.filter(Notice.school == session.get('school')).order_by(
                Notice.create_time.desc()).all()
        }
        return render_template('notice.html', **content)
    return render_template('notice.html', **content)


@app.route('/login/', methods=['GET', 'POST'])  # 登录界面
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.username
            session['score'] = user.score
            session['school'] = user.school
            session['time'] = time.time()  # 登录时间
            session.permanent = True
            # print('登录成功')
            return redirect(url_for('index'))
        else:
            return '手机号或密码错误'


@app.route('/manager/', methods=['GET', 'POST'])
@login_required
def manager():
    content = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('manager.html', **content)


@app.route('/logout/')  # 注销登录
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            # print('user')
            return {'user': user}
    #     print('user_id')
    # print('nothing')
    return {}


@app.route('/question/', methods=['GET', 'POST'])  # 提问
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        # 写入数据库
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')  # 获取id
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')  # 问题
@login_required
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    number_answer = len(question_model.answers)
    return render_template('detail.html', question_model=question_model, number_answer=number_answer)


@app.route('/news/<news_id>')  # 资讯页
def news_detail(news_id):
    news_model = News.query.filter(News.id == news_id).first()
    # number_answer = len(question_model.answers)
    return render_template('news_detail.html', news_model=news_model)


@app.route('/regist/', methods=['GET', 'POST'])  # 注册
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        school = request.form.get('school')
        # 手机号不能重复
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            print('手机号已被注册')
            return '手机号已被注册'
        else:
            if password != repassword:
                print('两次密码输入不一致')
                return '两次密码输入不一致'
            else:
                print('注册成功')
                user = User(telephone=telephone, username=username,
                            password=password, school=school, learn_time=0, score=0, active=1)  # 用户
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/add_answer/', methods=['POST'])  # 回答
@login_required
def add_answer():
    content = request.form.get('answer_content')
    answer = Answer(content=content)
    user_id = session['user_id']
    question_id = request.form.get('question_id')
    user = User.query.filter(User.id == user_id).first()
    question = Question.query.filter(Question.id == question_id).first()
    answer.author = user
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/user/<user_id>', methods=['get', 'post'])  # 用户主页
@login_required
def user(user_id):
    if request.method == 'GET':
        user_info = UserInfo.query.filter(UserInfo.user_id == user_id).first()  # 目标访问用户的信息
        if(user_info is None):  # 用户主页尚未设置。id=13，14为无效用户
            if(int(user_id) != session['user_id']):  # 访问别人主页
                user_info = UserInfo.query.filter(UserInfo.user_id == 13).first()  # 不可修改
            else:  # 自己访问自己主页
                user_info = UserInfo.query.filter(UserInfo.user_id == 14).first()  # 可初始化主页
        user = User.query.filter(User.id == session['user_id']).first()  # 当前登录的用户
        print(user_info)
        print(user)
        return render_template('user.html', user_info=user_info, user=user)

    else:
        signature = request.form.get('signature')
        birthday = request.form.get('birthday')
        user_id = session['user_id']
        user_info = UserInfo.query.filter(UserInfo.user_id == session['user_id']).first()
        if user_info:  # 先删除后增添
            db.session.delete(user_info)
            user_info = UserInfo(signature=signature, birthday=birthday, user_id=user_id)
            db.session.add(user_info)
        else:
            user_info = UserInfo(signature=signature, birthday=birthday, user_id=user_id)
            db.session.add(user_info)
        db.session.commit()
        print(user_info.signature)
        return redirect(url_for('index'))


@app.route('/news/', methods=['get', 'post'])  # 资讯
def news():
    if request.method == 'GET':
        content = {
            'news': News.query.order_by(News.date.desc()).all()
        }
        return render_template('news.html', **content)


@app.route('/rank/', methods=['get', 'post'])
def rank():
    if request.method == 'GET':
        num = len(User.query.order_by('score').all())
        content = {
            'users': User.query.order_by(User.score.desc()).all(),  # 用户
            'num': num  # 用户数
        }
        return render_template('rank.html', **content)


@app.route('/write_notice/', methods=['GET', 'POST'])  # 发布公告
@login_required
@manager_required
def write_notice():
    if request.method == 'GET':
        return render_template('write_notice.html')
    else:
        # 写入数据库
        title = request.form.get('title')
        content = request.form.get('content')
        school = session.get('school')
        notice = Notice(title=title, content=content, school=school)
        user_id = session.get('user_id')  # 获取id
        user = User.query.filter(User.id == user_id).first()
        notice.author = user
        db.session.add(notice)
        db.session.commit()
        return redirect(url_for('notice'))


@app.route('/write_news/', methods=['get', 'post'])
@login_required
@manager_required
def write_news():
    if request.method == 'GET':
        return render_template('write_news.html')
    else:
        # 写入数据库
        title = request.form.get('title')
        date = request.form.get('date')
        content = request.form.get('content')
        news = News(title=title, date=date, content=content)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news'))


if __name__ == '__main__':
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)