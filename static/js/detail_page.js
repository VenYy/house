$(document).ready(function () {
    $.ajax({
        type: "post",
        url: detail_url,
        success: function (facilities) {
            // 获取所有带有 class="facility" 的 li 元素
            var facilitiesElements = document.querySelectorAll('.facility');
            // 将 facilities 转换为集合，方便使用 includes() 方法
            var facilitiesSet = new Set(facilities);
            // 遍历每个 li 元素，检查其文本内容是否存在于 facilities 中
            facilitiesElements.forEach(function (element) {
                var facility = element.textContent.trim();
                if (!facilitiesSet.has(facility)) {
                    // 如果设施不在 facilities 中，则添加类名 not_in
                    element.classList.add('not_in');
                }
            });

        }
    })

    function rooms_chart() {
        const chart = echarts.init(document.getElementById("rooms"))
        $.ajax({
            type: "GET",
            dataType: "json",
            url: rooms_chart_url,
            success: function (data) {
                chart.setOption(data)
            }
        })
    }

    function address_chart() {
        const chart = echarts.init(document.getElementById("address"))
        $.ajax({
            type: "GET",
            dataType: "json",
            url: address_chart_url,
            success: function (data) {
                var options = {
                    xAxis: {
                        axisLabel: {
                            formatter: function (value) {
                                var ret = ""; // 拼接类目项
                                var maxLength = 1; // 每项显示文字个数
                                var valLength = value.length; // X轴类目项的文字个数
                                var rowN = Math.ceil(valLength / maxLength); // 类目项需要换行的行数
                                if (rowN > 1) // 如果类目项的文字个数大于3,
                                {
                                    for (var i = 0; i < rowN; i++) {
                                        var temp = ""; // 存放每次截取的字符串
                                        var start = i * maxLength; // 开始截取的位置
                                        var end = start + maxLength; // 结束截取的位置
                                        temp = value.substring(start, end) + "\n";
                                        ret += temp; // 拼接最终得到的字符串
                                    }
                                    return ret;
                                } else {
                                    return value;
                                }
                            },
                        }
                    },
                    series: [{
                        type: "bar",
                        itemStyle: {
                            normal: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                        offset: 0,
                                        color: '#00d386' // 0% 处的颜色
                                    }, {
                                        offset: 1,
                                        color: '#0076fc' // 100% 处的颜色
                                    }],
                                    globalCoord: false // 缺省为 false
                                },
                                barBorderRadius: [5, 5, 0, 0],
                            }
                        },
                    }]
                }
                chart.setOption(data)
                chart.setOption(options)
            }
        })
    }

    function price_chart() {
        const chart = echarts.init(document.getElementById("price"))
        $.ajax({
            type: "GET",
            dataType: "json",
            url: price_chart_url,
            success: function (data) {
                chart.setOption(data)
            }
        })
    }

    rooms_chart()
    address_chart()
    price_chart()

    // 用户点击收藏
    document.getElementById("add_star").addEventListener("click", function () {
        $.ajax({
            url: add_star_url,
            type: "get",
            dataType: "json",
            success: function (data) {
                if (data.code === 1) {
                    alert(data["info"])
                }
                else {
                    alert(data["error"])
                }
            }
        })
    })

})

