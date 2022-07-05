const log = function () {
    console.log.apply(console, arguments)
}

const e = function (sel) {
    return document.querySelector(sel)
}

const ajax = function (method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}
