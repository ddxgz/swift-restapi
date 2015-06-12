===========My:DEBUG:before add_user_role, 
 user:<User {u'id': u'b6e53837491d4343a523289e13ee435b', u'tenantId': u'a2d9e7951e1546c891824844aae7e4e1', u'enabled': True, u'name': u'testuser4', u'email': None}>, 
 role:<Role {u'id': u'3ec64ede69bb49f9aaa34d3b5b48d9bf', u'name': u'swifttestrole1'}>, 
 tenant:<Tenant {u'id': u'a2d9e7951e1546c891824844aae7e4e1', u'enabled': True, u'description': u'test4 tenant', u'name': u'test4'}>=========

===========My:DEBUG:REQ: curl -g -i -X PUT http://10.200.44.66:35357/v2.0/tenants/a2d9e7951e1546c891824844aae7e4e1/users/b6e53837491d4343a523289e13ee435b/roles/OS-KSADM/3ec64ede69bb49f9aaa34d3b5b48d9bf -H "User-Agent: python-keystoneclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}b521caa6e1db82e5a01c924a419870cb72b81635"=========

===========My:INFO:Starting new HTTP connection (1): 10.200.44.66=========

===========My:DEBUG:"PUT /v2.0/tenants/a2d9e7951e1546c891824844aae7e4e1/users/b6e53837491d4343a523289e13ee435b/roles/OS-KSADM/3ec64ede69bb49f9aaa34d3b5b48d9bf HTTP/1.1" 500 3422=========

===========My:DEBUG:RESP: [500] date: Fri, 12 Jun 2015 08:51:29 GMT content-length: 3422 content-type: text/plain connection: close 
RESP BODY: Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/eventlet/wsgi.py", line 389, in handle_one_response
    result = self.application(self.environ, start_response)
  File "/usr/lib/python2.7/dist-packages/paste/urlmap.py", line 203, in __call__
    return app(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 147, in __call__
    resp = self.call_func(req, *args, **self.kwargs)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 210, in call_func
    return self.func(req, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/keystone/common/wsgi.py", line 299, in __call__
    response = request.get_response(self.application)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1086, in get_response
    application, catch_exc_info=False)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1055, in call_application
    app_iter = application(self.environ, start_response)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 147, in __call__
    resp = self.call_func(req, *args, **self.kwargs)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 210, in call_func
    return self.func(req, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/keystone/common/wsgi.py", line 299, in __call__
    response = request.get_response(self.application)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1086, in get_response
    application, catch_exc_info=False)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1055, in call_application
    app_iter = application(self.environ, start_response)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 147, in __call__
    resp = self.call_func(req, *args, **self.kwargs)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 210, in call_func
    return self.func(req, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/keystone/common/wsgi.py", line 299, in __call__
    response = request.get_response(self.application)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1086, in get_response
    application, catch_exc_info=False)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1055, in call_application
    app_iter = application(self.environ, start_response)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 147, in __call__
    resp = self.call_func(req, *args, **self.kwargs)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 210, in call_func
    return self.func(req, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/keystone/common/wsgi.py", line 299, in __call__
    response = request.get_response(self.application)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1086, in get_response
    application, catch_exc_info=False)
  File "/usr/lib/python2.7/dist-packages/webob/request.py", line 1055, in call_application
    app_iter = application(self.environ, start_response)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 147, in __call__
    resp = self.call_func(req, *args, **self.kwargs)
  File "/usr/lib/python2.7/dist-packages/webob/dec.py", line 210, in call_func
    return self.func(req, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/keystone/common/wsgi.py", line 318, in __call__
    for line in req.body_file:
TypeError: 'LimitedLengthFile' object is not iterable

=========

===========My:DEBUG:Request returned failure status: 500=========
Traceback (most recent call last):
  File "keystonetst.py", line 52, in <module>
    kc.roles.add_user_role(testuser1, testrole, tenant=test1tenant, )
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/v2_0/roles.py", line 69, in add_user_role
    return self._update(route % params, None, "role")
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/base.py", line 219, in _update
    **kwargs)
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/adapter.py", line 179, in put
    return self.request(url, 'PUT', **kwargs)
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/adapter.py", line 206, in request
    resp = super(LegacyJsonAdapter, self).request(*args, **kwargs)
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/adapter.py", line 95, in request
    return self.session.request(url, method, **kwargs)
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/utils.py", line 336, in inner
    return func(*args, **kwargs)
  File "/home/pc/.local/lib/python2.7/site-packages/keystoneclient/session.py", line 397, in request
    raise exceptions.from_response(resp, method, url)
keystoneclient.openstack.common.apiclient.exceptions.InternalServerError: Internal Server Error (HTTP 500)
pc@pc-desktop:~/restapi$ curl -g -i -X PUT http://10.200.44.66:35357/v2.0/tenants/9496d2f257124344a5a985db2b5fc2f7/users/b376afc290db49b5a10b59729dd174fb/roles/OS-KSADM/3ec64ede69bb49f9aaa34d3b5b48d9bf -H "User-Agent: python-keystoneclient" -H "Accept: application/json" -H "X-Auth-Token: ADMIN"
HTTP/1.1 200 OK
Content-Type: application/json
Vary: X-Auth-Token
Date: Fri, 12 Jun 2015 08:53:40 GMT
Transfer-Encoding: chunked

{"role": {"id": "3ec64ede69bb49f9aaa34d3b5b48d9bf", "name": "swifttestrole1"}}pc@pc-desktop7124344a5a985db2b5fc2f7/users/b376afc290db49b5a10b59729dd174fb/roles/OS-KSADM/3ec64ede69bb49f9aaa34d3b5b48d9bf -H "User-Agent: python-keystoneclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}b521caa6e1db82e5a01c924a419870cb72b81635"
HTTP/1.1 401 Not Authorized
Content-Type: application/json
Vary: X-Auth-Token
Date: Fri, 12 Jun 2015 08:53:57 GMT
Transfer-Encoding: chunked

{"error": {"message": "The request you have made requires authentication.", "code": 401, "title": "Not Authorized"}}