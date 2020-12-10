function makeindex(token){
    var get_url = "http://127.0.0.1:8000/v1/users"
    var header_body = ''
    header_body += ' <div class="collapse navbar-collapse" id="navbarSupportedContent">';
    header_body += '<ul class="navbar-nav">';
    if (token){ 
        $.ajax({
            type:'get',
            url:get_url,
            dataType:'json',
            // 異部請求
            async : false,
            // 清除快取
            cache:false,
            beforeSend: function(request){   
                request.setRequestHeader("Authorization", token)},
            success:function(result){
                if(200 == result.code){
                    header_body +='<li class="nav-item active ">';
                    header_body +='<a class="nav-link url" href="/mylist">我的追蹤清單</a>';
                    header_body +='</li>'
                    header_body +='<li class="nav-item active ">';
                    header_body +='<a id="login_out" class="nav-link url" target="_blank" href="#">登出</a>';
                    header_body +='</li>'
                } else{
                    window.localStorage.removeItem('Pricecompare_token');
                    window.localStorage.removeItem('Pricecompare_user');
                    header_body += '<li class="nav-item active ">';
                    header_body += '<a class="nav-link url" href="/login">登入</a>';
                    header_body += '</li>';
                    header_body +='<li class="nav-item active ">';
                    header_body +='<a class="nav-link url" href="/register">註冊</a>';
                    header_body +='</li>';
                }
            }
        })       
    }else{
        header_body += '<li class="nav-item active ">';
        header_body += '<a class="nav-link url" href="/login">登入</a>';
        header_body += '</li>';
        header_body +='<li class="nav-item active ">';
        header_body +='<a class="nav-link url" href="/register">註冊</a>';
        header_body +='</li>';
        window.localStorage.removeItem('Pricecompare_token');
        window.localStorage.removeItem('Pricecompare_user');
    }
    header_body += '</ul>';
    header_body += '</div>';

    return header_body
}


function loginOut(){
    $('#login_out').on('click', function(){
            if(confirm("確定登出嗎?")){
                window.localStorage.removeItem('Pricecompare_token');
                window.localStorage.removeItem('Pricecompare_user');
                window.location.href= '/index';
            }
            else{
                location.reload()
            }
        }
    )
}

function cancel(event) {
    var bid=$(event).attr('id');
    var com_id=bid.split('@')[1];

    var token = window.localStorage.getItem('Pricecompare_token');
    var confirm=window.confirm('確認是否刪除') ;
    
    var get_url="http://127.0.0.1:8000/v1/mylist/delete";
    var post_data = {'com_id':com_id};
    if(confirm){
        $.ajax({
            type:"delete",
            url:get_url,
            dataType:"json",
            data:JSON.stringify(post_data),
            beforeSend: function(request) {      
            request.setRequestHeader("Authorization", token);
                                  },
            success:function(result){
            if (200 == result.code){
                alert('刪除成功')
                window.location.reload()
            }else{
             alert('錯誤')
            }
            }
        })
    }
}


$(document).ready(function (){
    $('.searchbt').on('click',function(){
        var keyword=$('.search').val()
        window.location = 'http://127.0.0.1:5000/search?keyword='+keyword+''
        
      })
    
})