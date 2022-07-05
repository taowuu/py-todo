const insertToList = function (todo) {
    let todoCell = todoTemplate(todo)
    let todoList = e('#id-todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

const todoDelete = function (e) {
    let self = e.target
    if(self.classList.contains('todo-delete')){
        let todoCell = self.parentElement
        let todo_id = todoCell.dataset.id
        apiTodoDelete(todo_id, function(r){
            todoCell.remove()
        })
    }
}

const insertUpdateForm = function (element) {
    let form = `
        <div class='todo-edit-form'>
            <input class='input-update'>
            <button class='button-update'>update</button>
        </div>
    `
    element.insertAdjacentHTML('beforeend', form)
}

const todoEdit = function (e) {
    let self = e.target
    if(self.classList.contains('todo-edit')){
        let element = self.parentElement
        insertUpdateForm(element)
    }
}

const updateTodoHtml = function (r) {
    let todo = JSON.parse(r)
    let selector = '#todo-' + todo.id
    let todoCell = e(selector)
    let titleSpan = todoCell.querySelector('.todo-title')
    titleSpan.innerHTML = todo.title
    updateForm = e('.todo-edit-form')
    updateForm.remove()
}

const updateDict = function (editForm) {
    let input = editForm.querySelector('.input-update')
    let title = input.value
    let todoCell = editForm.parentElement
    let todo_id = todoCell.dataset.id
    let form = {
        'id': todo_id,
        'title': title,
    }
    return form
}

const todoUpdate = function (event) {
    let self = event.target
    if(self.classList.contains('button-update')) {
        let editForm = self.parentElement
        let form = updateDict(editForm)
        apiTodoUpdate(form, function(r){
            updateTodoHtml(r)
        })
    }
}

const todoAdd = function () {
    let input = e('#id-input-todo')
    let title = input.value
    let form = {
        'title': title,
    }
    apiTodoAdd(form, function(r) {
        let todo = JSON.parse(r)
        insertToList(todo)
    })
    input.value = ''
}

//initial
const todoTemplate = function(todo) {
    let title = todo.title
    let id = todo.id
    let t = `
        <div class="todo-cell" id='todo-${id}' data-id="${id}">
            <button class="todo-edit">edit</button>
            <button class="todo-delete">delete</button>
            <span class='todo-title'>${title}</span>
        </div>
    `
    return t
}


const loadTodos = function () {
    apiTodoAll(function(r) {
        let todos = JSON.parse(r)
        for(let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertToList(todo)
        }
    })
}

const bindEvent = function (element, event, func) {
    element.addEventListener(event, func)
}

const bindEvents = function () {
    let addBtn = e('#id-button-add')
    bindEvent(addBtn, 'click', todoAdd)
    //
    let todoList = e('#id-todo-list')
    bindEvent(todoList, 'click', todoDelete)
    bindEvent(todoList, 'click', todoEdit)
    bindEvent(todoList, 'click', todoUpdate)
}

const __main = function () {
    loadTodos()
    bindEvents()
}

__main()
