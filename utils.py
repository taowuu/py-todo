def template(name):
    path = 'template/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def salted_password(password, salt='$!@><?>HUI&DWQa`'):
    def sha256(ascii_str):
        import hashlib
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
    hash1 = sha256(password)
    hash2 = sha256(hash1 + salt)
    return hash2


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(location, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    headers['Location'] = location
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def load_from_db(path):
    import json
    with open(path, 'r', encoding='utf-8') as f:
        b = f.read()
        return json.loads(b)


def save_to_db(data, path):
    import json
    b = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(b)


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    import random
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    from session import session
    from model.user import User
    username = session.get(session_id, '')
    u = User.find_by(username=username)
    return u


def json_response(data):
    # content-type 客户端可以忽略这个
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    import json
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def find_index(models, id):
    index = -1
    for i, e in enumerate(models):
        if e.id == id:
            index = i
            return index
    if index == -1:
        return index


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# def redirect(location):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     headers['Location'] = location
#     # 301 永久重定向 302 普通定向
#     # 302 状态码的含义, Location 的作用
#     header = response_with_headers(headers, 302)
#     r = header + '\r\n' + ''
#     return r.encode(encoding='utf-8')