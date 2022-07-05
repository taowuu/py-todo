from utils import (
    template,
    salted_password,
    redirect,
    random_str,
    response_with_headers,
)


def user_register(request):
    form = request.form_query()
    from model.user import User
    u = User.new(form)
    if u.validate_register() is not False:
        u.password = salted_password(u.password)
        u.save()
        return True
    else:
        return False


def register(request):
    if request.method == 'POST':
        if user_register(request) is True:
            return redirect('/login')
        else:
            return redirect('/register')
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('register.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def user_login(request, headers):
    form = request.form_query()
    from model.user import User
    u = User.new(form)
    if u.validate_login():
        user = User.find_by(username=u.username)
        session_id = random_str()
        from session import session
        session[session_id] = user.username
        headers['Set-Cookie'] = 'user={}'.format(session_id)
        return True


def login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    #
    if request.method == 'POST':
        if user_login(request, headers) is True:
            return redirect('/todo', headers)
        else:
            return redirect('/login')
    body = template('login.html')
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def logout(request):
    from session import session
    session.clear()
    print(session)
    return redirect('/login')


route_dict = {
    '/register': register,
    '/login': login,
    '/logout': logout,
}
