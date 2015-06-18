swift-webstorage-restapi
================
This is REST API for wrapping Openstack Swift as a web storage, can be used by clients which do not require synchronization. 

Credit to github.com/cschwede/django-swiftbrowser


Functions
---------------
- Download/upload files from/to Swift
- Share files with links
- Provide API for clients of other platforms


API v1:
---------------

####Files
#####GET

> /v1/disk/
>> return a json contains metadate and all the files and folds

> /v1/disk/{path2file or path}
>> return a tempo_url which can download the file

#####PUT

> /v1/disk/{path2file or path}
>> return a storage_url and auth_token which can be used to PUT the file to the storage_url with auth_token in the header

#####DELETE
> /v1/disk/{path2file or path}
>> return an info tells whether the delete success or not


####Account
#####GET
> /v1/account/
>> return a json contains info of the user account


#####POST
> /v1/account/
>> return an info whether the account create success or not


Configuration
---------------
Support both Swift tempauth and keystoneauth, specified by 'auth_version' in config file. '1' for tempauth and '2' for keystoneauth.


TODO
---------------
- ~~Multi-user support, need to integrate keystone~~
- Verify if the request if ok, such as if the file exists when get,
	or the path2file is a fold
- set the temp_key expires time based on the size of target file
- handling large files 
- deal with when file with prefix dir upload to swift without pseudo fold created, need to create a pseudo first. This is not a problem when used by android client
- report keystone add_user_role bug
- handle fold rename and file rename
- add ACL per container per user


BUG
---------------
- There are problems with python-keystoneclient's add_user_role and delete_user, used curl command instead.


Notifications
---------------
- when add a new role, need to add that role name to swift's proxy-server.conf


Requirements
---------------
The environment is organized as a docker container, locates in docker-compose/,
just docker-compose up. The port can be changed as you like in docker-compose.yml

- Python >= 2.7 or 3.4
- python-swiftclient >= 2.4.0
- python-keystoneclient >= 1.4.0
- Gunicorn or uWsgi
- Falcon >= 0.3.0
- peewee >= 2.6.1
- curl
