function register() {
        var formdata = {
            "username": $("#username").val(),
            "password": $("#password").val(),
            "nickname": $("#nickname").val()
        }
        $.ajax({
            url: "/register",
            data: JSON.stringify(formdata),
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                if (result.result == "OK") {
                    toastr["success"]("注册成功")
                    window.location.href = "/login"
                } else if (result.result == "NO") {
                    toastr["error"](result.msg)
                }
            },
            error: function () {
                toastr["error"]("网络连接失败");
            }
        })
    }