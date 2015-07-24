swift-webstorage-restapi
================
This is REST API for wrapping Openstack Swift as a web storage, can be used by clients which do not require synchronization.

Credit to github.com/cschwede/django-swiftbrowser


Functions
---------------
- Download/upload files from/to Swift
- Share files with links (by tempurl)
- Provide API for clients of other platforms


API v1:
---------------
All the requests need username and password in the header:
```
{
    'username': username,
    'password': password,
    ...
}
```

####Files
#####GET

> `/v1/disk/`
>> return a json contains metadate and all the files and folds

> `/v1/disk/{path2file or dir}`
>> if it's path2file, it will return a tempo_url which can download the file, and if it's dir, it will return all the files and dirs under it.
>>> if request a dir, put the path in the header `dir`

#####PUT

> `/v1/disk/{path2file or dir}`
>> Return a storage_url and auth_token which can be used to PUT the file to the storage_url with auth_token in the header.

>> When put a dir, put the path in the header `dir`, which is the part after v1/disk/, for instance:
   ```
{
	'username': username,
	'password': password,
	'dir':fold1
}
   ```


#####POST
> `/v1/disk`
>> to copy or move files, post with data like this:
```
{
 'disk':[
            {
            'from':'fold1/subfold2/curl.py',
            'copy':'pics2/cnew3.conf'
            },
            {
            'from':'fold1/subfold1/models.py',
            'move':'pics/new.png'
            },
            {
            'from':'config.py',
            'copy':'pics3/cnew4.conf'
            }
        ]
}
```

#####DELETE
> `/v1/disk/{path2file or path}`
>> return an info tells whether the delete success or not


####Account
#####GET
> `/v1/account/`
>> return a json contains info of the user account


#####PUT
> `/v1/account/`
>> return an info whether the account create success or not


#####POST
> `/v1/account`
>> to change user's data, post with data like this:
```
{
 'email': {
            'from':'user1@email.com',
            'to':'user2@email.com'
          }
}
```

#####DELETE
> `/v1/account/`
>> return an info whether the account deleted success or not


Configuration
---------------
Support both Swift tempauth and keystoneauth, specified by `auth_version` in config file. `1` for tempauth and `2` for keystoneauth.


TODO
---------------
- ~~change endpoint create~~
- use a separated user auth module (may use the swift's tempauth like method, which uses memcache to store token, set a expire time on each token, or the auth middleware <https://github.com/talons/talons>)
- add test for copy and move
- functest, probtest, unittest
- ~~seperated dir refresh~~
- deal with the security of password storing and transferring
- ~~DELETE /v1/account~~
- ~~Multi-user support, need to integrate keystone~~
- Verify if the request if ok, such as if the file exists when get,
	or the path2file is a fold
- set the temp_key expires time based on the size of target file
- handling large files
- deal with when file with prefix dir upload to swift without pseudo fold created, need to create a pseudo first. But this is not a problem when used by android client
- ~~handle fold rename and file rename by X-Copy-From header~~
- add ACL per container per user


BUG
---------------
- There are problems with python-keystoneclient's add_user_role and delete_user, used curl command instead.


Notice
---------------
- when add a new role, need to add that role name to swift's /etc/swift/proxy-server.conf


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
- Six >= 1.9
- curl
