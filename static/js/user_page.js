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

    $.ajax({
        type: "get",
        dataType: "json",
        url: "http://127.0.0.1:5000/stars",
        success: function (data) {
            console.log(data);
            if (data.code === 1) {
                const stars = data["stars"];
                const stars_list = document.getElementById("stars_list");
                let str = "";
                for (let i = 0; i < stars.length; i++) {
                    if (!stars[i].direction) {
                        stars[i].direction = "暂无数据"
                    }
                    if (!stars[i].traffic) {
                        stars[i].traffic = "暂无数据"
                    }
                    str += '<li>';
                    str += '<a href="/house/' + stars[i].id + '" style="text-decoration: none"><img class="img_view" src="/static/images/house-bg1.jpg" alt=""></a>';
                    str += '<div class="right">';
                    str += '<p><a href="/house/' + stars[i].id + '" style="text-decoration: none"><span class="title">' + stars[i].title + '</span><span class="price">￥' + stars[i].price + '</span></a></p>';
                    str += '<p>房源地址：<span class="address">' + stars[i].address + '</span></p>';
                    str += '<p>房源户型：<span class="rooms">' + stars[i].rooms + '</span></p>';
                    str += '<p>房源朝向：<span class="direction">' + stars[i].direction + '</span></p>';
                    str += '<p>交通条件：<span class="traffic">' + stars[i].traffic + '</span></p>';
                    str += '<p><img class="like" src="/static/images/like.png" alt="">' + stars[i].page_views + '人浏览过</p>';
                    str += '</div>';
                    str += '</li>';
                }
                stars_list.innerHTML += str;
            } else {
                document.getElementById("stars_list").innerHTML = "<div class='tip'>暂无收藏</div>"
            }
        }

    })

    $.ajax({
        type: "get",
        dataType: "json",
        url: "http://127.0.0.1:5000/views",
        success: function (data) {
            if (data.code === 0) {
                document.getElementById("views_list").innerHTML = "<div class='tip'>暂无浏览历史</div>"
            } else {
                console.log(data)
                const views = data["views"]
                const views_list = document.getElementById("views_list")
                let str = ""
                for (let i = 0; i < views.length; i++) {
                    str += `<p><span class="title"><a href="/house/${views[i].id}">${views[i].title}</a></span><span class="price">￥${views[i].price}</span></p>`
                }
                views_list.innerHTML = str
            }
        }
    })


})


