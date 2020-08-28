function chose_prodc(pid) {
        var formdata = {
            "pid": pid,
        }
        $.ajax({
            url: "/add",
            type: "POST",
            data: JSON.stringify(formdata),
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                if (result.result == "OK") {
                    toastr["success"]("添加成功")
                } else if (result.result == "NO") {
                    toastr["error"]("添加失败")
                }
            },
            error: function () {
                toastr["error"]("网络连接失败");
            }
        })
    }