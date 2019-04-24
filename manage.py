#-*-coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User, Question
manager = Manager(app)

#使用Migrate绑定app，db
migrate = Migrate(app, db)

#添加迁移脚本命令到Migrate
manager.add_command('db',MigrateCommand)





if __name__ == '__main__':
    manager.run()