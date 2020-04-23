from extra import db
from datetime import datetime


# 更新指令 python manager.py db migrate -> python manager.py db upgrade

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100))
    active = db.Column(db.Integer)

    learn_time = db.Column(db.Integer)  # 学习时长
    learn_content = db.Column(db.String(50))  # 学习内容(资源分区)
    score = db.Column(db.Integer)  # 积分=答题得分-答错扣分+学习时长*权重


class SignIn(db.Model):
    __tablename__ = 'sign_in'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.now())  # 签到时间
    num = db.Column(db.Integer)  # 连续天数

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sign_in'))


# 反馈表
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    reply = db.Column(db.Text)  # 回复
    manager_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now())
    reply_time = db.Column(db.DateTime)  # 回复时间

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('feedbacks'))  # 用户


# 问题表
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()服务器第一次运行时间， now每次创建时的当前时间
    create_time = db.Column(db.DateTime, default=datetime.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))  # question.author


# 回复表
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author = db.relationship('User', backref=db.backref('answers'))
    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))


# 用户资料表
class UserInfo(db.Model):
    __tabelname__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    signature = db.Column(db.Text, nullable=False)
    birthday = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user_info'))  # user_info.user


# 通知
class Notice(db.Model):
    __tabelname__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)  # 通知标题
    content = db.Column(db.Text, nullable=False)  # 通知内容
    # now()服务器第一次运行时间， now每次创建时的当前时间
    create_time = db.Column(db.DateTime, default=datetime.now())
    school = db.Column(db.String(100))  # 通知适用范围

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('notices'))  # 外链(通知者)


# 垃圾
class Garbage(db.Model):
    __tabelname__ = 'garbage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    code_id = db.Column(db.Integer)  # 分类代码
    code_name = db.Column(db.String(50), nullable=False)  # 分类名称


# 视频资源
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)  # 标题
    link = db.Column(db.String(200), nullable=False)  # 链接
    duration = db.Column(db.String(50), nullable=False)  # 时长
    code_id = db.Column(db.Integer)  # 平台分类代码，1:腾讯视频；2：bilibili


# 资讯
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)  # 标题
    date = db.Column(db.String(50), nullable=False)  # 日期
    content = db.Column(db.Text, nullable=False)  # 内容
