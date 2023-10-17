// 创建一个数据库及对象存储空间来存储用户的信息
const request = window.indexedDB.open("users", 1);
request.onupgradeneeded = function (event) {
    const db = event.target.result;
    const objectStore = db.createObjectStore("users", {keyPath: "id", autoIncrement: true});
    objectStore.createIndex("username", "username", {unique: true});
};


// 注册用户
function registerUser(username, password, callback) {
    const request = window.indexedDB.open("users", 1);
    request.onsuccess = function (event) {
        const db = event.target.result;
        const transaction = db.transaction(["users"], "readwrite");
        const objectStore = transaction.objectStore("users");
        const user = {username: username, password: password};
        const addUser = objectStore.add(user);
        addUser.onsuccess = function (event) {
            console.log("成功添加用户");
            if (callback) callback(true);
        };
        addUser.onerror = function (event) {
            console.log("添加用户失败");
            if (callback) callback(false);
        };
    };
}

// 验证登录信息
function loginUser(username, password, callback) {
    const request = window.indexedDB.open("users", 1);
    request.onsuccess = function (event) {
        const db = event.target.result;
        const transaction = db.transaction(["users"], "readonly");
        const objectStore = transaction.objectStore("users");
        const index = objectStore.index("username");
        const getUser = index.get(username);
        getUser.onsuccess = function (event) {
            var user = event.target.result;
            if (user && user.password === password) {
                console.log("User logged in successfully.");
                if (callback) callback(true);
            } else {
                if (callback) callback(false);
            }
        };
        getUser.onerror = function (event) {
            if (callback) callback(false);
        };
    };
}


// 获取表单元素与按钮
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

if (loginForm) {

    //
    var transBtn = document.getElementById("trans")
    transBtn.innerText = "注册"
    transBtn.addEventListener("click", () => {
        window.location = register_url
    })

    document.getElementById("title").innerText = "登录"


    // 绑定表单提交事件
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // 防止表单提交刷新页面

        // 获取输入的用户名和密码
        const username = document.getElementById('uname').value;
        const password = document.getElementById('pwd').value;

        // 调用登录函数进行验证
        loginUser(username, password, function (result) {
            if (result) {
                // 登录成功
                // 添加cookie信息
                var now = new Date();
                var time = now.getTime();
                var expireTime = time + 1000 * 60 * 30;
                document.cookie = `user=${username}=loggedIn; expires=${expireTime}; path=/`;
                window.location = index_url
            } else {
                alert("用户名或密码不正确");
            }
        });
    });

    // 优化不同页面的展示效果
    loginForm.style.marginTop = "30px"


}
if (registerForm) {

    //
    // 登录和注册页面不同的样式修改
    var transBtn = document.getElementById("trans")
    transBtn.innerText = "登录"
    transBtn.addEventListener("click", () => {
        window.location = login_url
    })
    document.getElementById("title").innerText = "注册"

    var inputs = document.querySelectorAll("input")
    inputs.forEach(input => {
        input.style.height = "40px"
    })


    registerForm.addEventListener('submit', function (event) {
        event.preventDefault(); // 防止表单提交刷新页面

        // 获取输入的用户名、密码和确认密码
        const username = document.getElementById('uname').value;
        const password = document.getElementById('pwd').value;
        const confirmPwd = document.getElementById('confirm-pwd').value;

        // 确认密码是否匹配
        if (password !== confirmPwd) {
            alert("两次输入的密码不匹配，请重新输入！");
            return;
        }
        // 调用注册函数进行添加
        registerUser(username, password, function (result) {
            if (result) {
                // alert("注册成功！");
                loginSuccessTip()
            } else {
                alert("用户名已存在！");
            }
        })
    })
}


// 注册成功后显示的内容提示框
function loginSuccessTip() {
    var successAlert = document.getElementById("success-alert")
    successAlert.style.display = "block"
    // 等待 3 秒后跳转到登录页面
    var count = 2;
    var timer = setInterval(function () {
        count--;
        document.getElementById("count").innerHTML = `<a href={login_url}>剩余: ${count + 1}s</a>`;
        if (count === 0) {
            clearInterval(timer);
            window.location = login_url
        }
    }, 1000);
}




// 用户登录时展示的内容