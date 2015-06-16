import logging
import datetime

from peewee import SqliteDatabase, Model, CharField, BooleanField, IntegerField

from config import Config
from myexceptions import UserNotExistException, PasswordIncorrectException


logging.basicConfig(format='===========My:%(levelname)s:%(message)s=========', 
    level=logging.DEBUG)


conf = Config()
# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase('account.sqlite3')

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database


class AccountModel(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = CharField()
    account_level = IntegerField()
    keystone_tenant = CharField()
    keystone_username = CharField()
    keystone_password = CharField()
    # username_service, eg. tester_disk
    disk_container = CharField()
    keystone_info = CharField()

    class Meta:
        order_by = ('username',)

    @classmethod
    def auth(cls, username, password):
        logging.debug('in auth')

        try:
            user = AccountModel.get(AccountModel.username==username, 
                             AccountModel.password==password)

        except:
            logging.debug('in model, got old_user')
            old_user = AccountModel.get(AccountModel.username==username)
            if old_user:
                raise PasswordIncorrectException()
            else:
                logging.debug('in model, not got old_user')

                raise UserNotExistException()
        else:
            logging.debug('after ger user%s'%user.username)
            return user


def create_tables():
    database.connect()
    database.create_tables([AccountModel], safe=True)


def test():
    # AccountModel.create(username='username', 
    #                 password='password',
    #                 email='email',
    #                 join_date=str(datetime.datetime.now())+' GMT+8',
    #                 account_level=0)
    logging.debug('in account post create except')

            # `username` is a unique column, so this username already exists,
            # making it safe to call .get().
    old_user = AccountModel.get(AccountModel.username == 'user1')
    logging.debug('user exists:%s'%old_user.email)


# create_tables()

# test()