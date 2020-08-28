function delete_prodc(pid) {
        toastr["success"](pid)
        var formdata = {
            "pid": pid,
        }
        $.ajax({
            url: "/delete",
            type: "POST",
            data: JSON.stringify(formdata),
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                if (result.result == "OK") {
                    toastr["success"]("添加成功")
                    window.location.href = "/shoppingcar"
                } else if (result.result == "NO") {
                    toastr["error"]("添加失败")
                }
            },
            error: function () {
                toastr["error"]("网络连接失败");
            }
        })
    }

    function create_his(pid) {
        toastr["success"]("创建成功")
        var formdata = {
            "pid": pid,
        }
        $.ajax({
            url: "/create",
            type: "POST",
            data: JSON.stringify(formdata),
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                if (result.result == "OK") {
                    toastr["success"]("添加成功")
                    window.location.href = "/shoppingcar"
                } else if (result.result == "NO") {
                    toastr["error"]("添加失败")
                }
            },
            error: function () {
                toastr["error"]("网络连接失败");
            }
        })
    }