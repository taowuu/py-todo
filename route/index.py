def index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    from utils import template
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': index,
}