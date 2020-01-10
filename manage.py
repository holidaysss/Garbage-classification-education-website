from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from MacRae import app
from extra import db
from models import User, Question, Answer, UserInfo


manager = Manager(app)

# 用Migrate绑定app，db
migrate = Migrate(app, db)

# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()