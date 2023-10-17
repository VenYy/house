$(document).ready(function () {
    $("#username_input").hide()
    $("#address_input").hide()
    $("#password_input").hide()
    $("#email_input").hide()
    $(".submit_btn").hide()

    $(".edit_btn").on("click", function (event) {
        event.preventDefault()
        $("#username_input").show()
        $("#address_input").show()
        $("#password_input").show()
        $("#email_input").show()
        $(".col span:nth-child(2)").hide()
        $(".edit_btn").hide()
        $(".submit_btn").show()

    })

    function save_user(event) {
        event.preventDefault()
        // 获取用户输入的数据
        var form = $("#user_info")
        var username = form.find('input[name="i_username"]').val();
        var address = form.find('input[name="i_address"]').val();
        var password = form.find('input[name="i_password"]').val();
        var email = form.find('input[name="i_email"]').val();
        // console.log(username, address, password, email);


        // 打开数据库连接
        const request = indexedDB.open("users", 1);
        request.onsuccess = function (e) {
            const db = e.target.result;
            const transaction = db.transaction(["users"], "readwrite");
            const store = transaction.objectStore("users");

            const index = store.index("username");
            // console.log(index.get("username"))

            const request = index.get(current_user);
            // console.log(request)

            request.onsuccess = (e) => {
                const matchingRecord = e.target.result;

                if (!matchingRecord) {
                    return
                }

                if (matchingRecord) {
                    // 向现有记录添加新数据
                    if (username) matchingRecord.username = username;
                    if (address) matchingRecord.address = address;
                    if (password) matchingRecord.password = password;
                    if (email) matchingRecord.email = email;

                    // 将更新的记录写回 IndexedDB
                    store.put(matchingRecord);
                }
                alert("成功更新信息");
                location.reload()
            };

            request.onerror = () => {
                alert("更新信息失败");
            };
        };
    }

    $(".submit_btn").on("click", save_user)

})


