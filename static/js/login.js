function login() {
        var formdata = {
            "username": $("#username").val(),
            "password": $("#password").val(),
        }
        $.ajax({
            url: "/login",
            type: "POST",
            data: JSON.stringify(formdata),
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                if (result.result == "OK") {
                    toastr["success"]("登录成功")
                    setTimeout(next_url(result.next_url), 3000);
                } else if (result.result == "NO") {
                    toastr["error"](result.msg)
                }
            },
            error: function () {
                toastr["error"]("网络连接失败");
            }
        })
    }

    function next_url(url) {
        window.location.href = url;
    }