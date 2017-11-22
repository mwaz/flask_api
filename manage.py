"""Handles DB migrations and upgrade in postgres"""
import os
import unittest
from flask_script import Manager
 # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, make_app
from app import models

app = make_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """metod to define how to run tests within the tests directory"""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    results = unittest.TextTestRunner(verbosity=2).run(tests)
    if results.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()