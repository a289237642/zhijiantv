# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 1:34 PM
# @Author  : Shande
# @Email   : seventhedog@163.com
# @File    : manage.py
# @Software: PyCharm

from flask_migrate import Migrate, MigrateCommand
from app import create_app
from flask_script import Manager

app, db = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
