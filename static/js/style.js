function showHouseTopic() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/",
        dataType: "text",
        success: function (data) {
            console.log(data)
        },
        error: function (xml, status, error) {
            console.log("error")
            console.log(xml.status)
            console.log(error)
        }
    })
}

// showHouseTopic()
var search_content = document.getElementById("search_content")

$(document).ready(function () {
    // 点击按钮切换输入框显示的内容
    $("#search_by_address").click(function () {
        $("#search_content").attr("placeholder", "请输入区域、商圈或小区名开始找房")
        $("#search_content").attr("name", "addr")
        $("#search_by_address").addClass("search_active")
        $("#search_by_rooms").removeClass("search_active")
    })
    $("#search_by_rooms").click(function () {
        $("#search_content").attr("placeholder", "请输入户型开始找房, 例如1室1厅")
        $("#search_content").attr("name", "rooms")
        $("#search_by_rooms").addClass("search_active")
        $("#search_by_address").removeClass("search_active")
    })
    // 设置锁，true表示锁住输入框，false表示解锁输入框
    var cpLock = false;

    // 中文搜索，监听compositionstart事件，如果触发该事件，就锁住输入框
    $('#search_content').on('compositionstart', function () {
        cpLock = true;
    });

    // 中文搜索，监听compositionend事件，如果触发该事件，就解锁输入框
    $('#search_content').on('compositionend', function () {
        cpLock = false;
        var keyWord = search_content.value;
        var resultList = search_by_indexOf(keyWord);
    });

    // 英文搜索，监听input事件，用于处理字母搜索
    $('#search_content').on('input', function () {
        if (!cpLock) {
            var keyWord = search_content.value;
            var resultList = search_by_indexOf(keyWord);
        }
    });

})


function search_by_indexOf(keyword) {
    $(".nav_tab li").each(function (index, element) {
        // 判断用户所选择的搜索类型
        if ($(this).hasClass("search_active")) {
            var search_type = $(this).text()
            var data = {"keyword": keyword, "search_type": search_type}
            console.log(data)

            $.ajax({
                url: "http://127.0.0.1:5000/search/keyword/",
                dataType: "json",
                type: "post",
                data: data,
                success: function (data) {
                    console.log(data)
                    var search_result = document.getElementById("search_result")
                    var txt = ""
                    if (data["code"] === 0) {
                        // alert("未找到关于" + keyword + "的房屋信息")
                        // search_content.value = ""
                    } else {
                        for (let i = 0; i < data["data"].length; i++) {
                            txt += `<li class="result_list" title="${data['data'][i]['name']}"><span class="name">${data["data"][i]["name"]}</span>
                                    <span class="val">有${data["data"][i]["count"]}套房</span></li>`
                        }
                    }
                    search_result.innerHTML = txt
                    info_to_txt()
                    if (search_content.value.length === 0) {
                        search_result.innerHTML = ""
                    }
                    return data["data"]

                }
            })

        }

    })
}

// 点击检索候选区将其填入输入框
function info_to_txt() {
    $(".result_list").on("click", function () {
        // 重复点击初始化
        if ($(this).hasClass("active")) {
            $(this).removeClass("active")
        }
        $(this).addClass("actice")
        t_name = $(this).attr("title")
        $("#search_content").val("")
        $("#search_content").val(t_name)
        $("#search_result").empty()
    })
}