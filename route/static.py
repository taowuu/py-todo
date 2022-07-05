# def static(request):
#     filename = request.query.get('file', )
#     type = filename.split('.')[-1]
#     if type == 'js':
#         path = 'static/js/' + filename
#     elif type == 'css':
#         path = 'static/css/' + filename
#     else:
#         path = 'static/img/' + filename
#     with open(path, 'rb') as f:
#         header = b'HTTP/1.1 200 OK\r\n\r\n'
#         fs = header + f.read()
#         return fs


def js_static(request):
    filename = request.query.get('file')
    path = 'static/js/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        fs = header + f.read()
        return fs


def img_static(request):
    filename = request.query.get('file')
    path = 'static/img/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        fs = header + f.read()
        return fs


route_dict = {
    # '/static': static,
    '/static/js': js_static,
    '/static/img': img_static,
}