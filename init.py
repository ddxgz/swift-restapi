
"""
init related configurations
create db
create keystone things
"""
import logging

from config import Config
from keystonewrap import create_service, create_role
from models import create_tables

logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')


conf = Config()

create_tables()
# create_service()
# create_role(conf.swift_role)