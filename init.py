
"""
init related configurations
create db
create keystone things
"""
from config import Config
from keystonewrap import create_service, create_role

conf = Config()

create_service()
create_role(conf.swift_role)