class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        # print(kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        self.add_cookies()

    def form_query(self):
        args = self.body.split('&')
        f = {}
        import urllib.parse
        for arg in args:
            k, v = urllib.parse.unquote(arg).split('=')
            f[k] = v
        return f

    def form_body(self):
        import json
        return json.loads(self.body)
