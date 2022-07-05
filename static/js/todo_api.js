const apiTodoAll = function(callback) {
    let path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

const apiTodoAdd = function(form, callback) {
    let path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

const apiTodoDelete = function(id, callback) {
    let path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
}

const apiTodoUpdate = function(form, callback) {
    let path = '/api/todo/update'
    ajax('POST', path, form, callback)
}
