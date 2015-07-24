import ast
import urllib2
import requests
import logging

# logging.basicConfig(format='===========%(levelname)s:%(message)s=========', 
#     level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')


class Visit():
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers, 
            data=data)
        req.get_method = lambda: 'PUT'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put_file(self, filename='', suffix_url='', headers=None, data=None):
        code_url, resp_str = self.put(suffix_url=suffix_url, headers=headers)
        resp = ast.literal_eval(resp_str)
        logging.debug('resp:%s' % (resp))
        token = resp.get('auth_token')
        storage_url = resp.get('storage_url')
        headers = {'x-storage-token':token}
        files = {'file': open(filename)}
        put_resp = requests.put(storage_url, files=files, headers=headers)
        page = put_resp.headers
        code = put_resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


    def post(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, 
            headers=headers, data=data)
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page


    def delete(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers, 
            data=data)
        req.get_method = lambda: 'DELETE'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

