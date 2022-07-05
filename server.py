def register_route():
    from route.index import route_dict as index
    from route.static import route_dict as static
    from route.user import route_dict as user
    from route.todo import route_dict as todo
    r = {}
    r.update(index)
    r.update(static)
    r.update(user)
    r.update(todo)
    return r


def parsed_request(r):
    r = r.decode('utf-8')
    path = r.split()[1]
    #
    from request import Request
    request = Request()
    request.method = r.split()[0]
    request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
    request.body = r.split('\r\n\r\n', 1)[1]
    return path, request


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    #
    r = register_route()
    from utils import error
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1024)
    # 防止浏览器发送空请求导致程序崩溃
    if len(r.split()) < 2:
        connection.close()
    path, request = parsed_request(r)
    response = response_for_path(path, request)
    connection.sendall(response)
    connection.close()


def run(host='', port=3000):
    import socket
    import _thread
    # with 可保证程序中断时关闭 socket
    # 释放 socket 占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(3)
        while True:
            connection, address = s.accept()
            # tuple 如果只有一个值 必须带逗号
            # 对每个请求开启新的线程进行处理
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # __name__ 是当前模块名
    # 当模块被运行时 __name__ 为 __main__
    # 防止 run 在该文件被 import 时执行
    config = dict(
        host='',
        port=3000,
    )
    # ** 可将字典 kv 与函数参数匹配
    run(**config)
