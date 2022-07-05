from utils import (
    template,
    current_user,
    json_response,
    redirect,
)

from model.todo import Todo


def todo(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('todo.html')
    u = current_user(request)
    if u is None:
        return redirect('/login')
    result = u.username
    body = body.replace('{{ username }}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def all(request):
    u = current_user(request)
    todo_list = Todo.find_all(username=u.username)
    todos = [t.dict_form() for t in todo_list]
    return json_response(todos)


def add(request):
    form = request.form_body()
    u = current_user(request)
    form['username'] = u.username
    t = Todo.new(form)
    t.save()
    return json_response(t.dict_form())


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.dict_form())


def update(request):
    form = request.form_body()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.dict_form())


route_dict = {
    '/todo': todo,
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
}