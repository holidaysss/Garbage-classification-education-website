from functools import wraps
from flask import session, redirect, url_for


# 登录限制装饰器
def login_required(func):
    @wraps(func)  # 保护函数属性
    def wrapper(*args, **kwargs):
        if session.get('user_id'):  # 判断是否登录
            return func(*args, **kwargs)  # return到外面
        else:
            return redirect(url_for('login'))
    return wrapper
