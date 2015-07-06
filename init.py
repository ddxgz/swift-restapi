
"""
init related configurations
create db
create keystone things
"""
from config import Config
from keystonewrap import create_service, create_role
from models import create_tables

conf = Config()

create_tables()
create_service()
create_role(conf.swift_role)