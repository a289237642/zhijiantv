# -*- coding:utf-8 -*-
# manager.py主要管理程序的启动，以及db的操作
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app import create_app
from config.config import DevelopmentConfig, ProductionConfig

app, db = create_app(ProductionConfig)
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
