var log = {
    startdt: "2020-10-2",
    enddt: "2020-10-5",
    upatedt: "2020-10-5",
    anchor: "Sam",
    url:"http://127.0.0.1:8000/",
}
//對象邏輯
log.submit = {
    check: function (v) { //驗證是否為空
        var _v = (v == "") ? true : false;
        return _v;
    },
    autohide:function(obj){
        setTimeout(function(){
             obj.css('visibility', 'hidden');
        },2000)
    }
}
//驗證是否為空的函數
function checkvalue() {
    //會取元素對象 保存數據
    var $username = $("#username");
    var $email=$('#email');
    var $password1 = $("#password1");
    var $password2 = $("#password2");
    var $err1 = $("#err1");
    var $err2 = $("#err2");
    var $err3 = $("#err3");
    var $err4 = $("#err4");

    // 當用戶明和密碼都不為空時
    if (!log.submit.check($username.val()) && !log.submit.check($email.val()) && !log.submit.check($password1.val()) && !log.submit.check($password2.val()) ) {
        //直接提交
        var username = $('.username').val()
        var email = $('.email').val()
        var password_1 = $('.password_1').val()
        var password_2 = $('.password_2').val()
        var post_data = {'username':username, 'email':email, 'password_1':password_1, 'password_2':password_2}
        $.ajax({
            // 請求方式
            type:"post",
            // contentType 
            contentType:"application/json",
            // dataType
            dataType:"json",
            // url
            url:log.url+"v1/users/register",
            // 把JS的對象或數組序列畫一個json 字符串
            data:JSON.stringify(post_data),
            // result 為請求的返回結果對象
            success:function (result) {
                if (200 == result.code){
                    window.localStorage.setItem('Pricecompare_token', result.data.token)
                    window.localStorage.setItem('Pricecompare_user', result.username)
                    alert("註冊成功 點擊可以跳轉主頁")
                    window.location.href = '/'+'index'
                }else{
                    alert(result.error)
                }
            }
        });
    } else {
        //如果用戶名為空
        if ($username.val() == "") {
            //提示如果用戶名為空的錯誤顯示
            $err1.css('visibility', 'visible');
            //2秒後自動隱藏
            log.submit.autohide($err1);
            //阻止提交
        } 
        if ($email.val() == "") {
            //提示信箱為空的錯誤顯示
            $err2.css('visibility', 'visible');
            //2秒後自動隱藏
            log.submit.autohide($err2);
            //阻止提交
        } 
        if ($password1.val() == "") {
            //提示密碼為空的錯誤顯示
            $err3.css('visibility', 'visible');
            //2秒後自動隱藏
            log.submit.autohide($err3);
            //阻止提交
        } 
        if ($password2.val() == ""){
            //提示密碼為空的錯誤顯示
            $err4.css('visibility', 'visible');
            //2秒後自動隱藏
            log.submit.autohide($err4);
            //阻止提交
        }
    }
}