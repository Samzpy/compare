$(document).ready(function (){
    var url = document.location.toString();    
    var arrUrl =url.split("//");
    var com_id= arrUrl[1].split('/')[2];
    var get_url = "http://127.0.0.1:8000/v1/detail?com_id=" + com_id;

    var token = window.localStorage.getItem('Pricecompare_token');
    $.ajax({
        type:"get",
        url:get_url,
        dataType:"json",
        beforeSend: function(request) {      
        request.setRequestHeader("Authorization", token)
        },
        success:function(result){
            // 判定是否成功
            if (200 == result.code){
                // 判定是否為追蹤
                if(1 == result.com_track){
                    $('button[class="com_track"]').text("取消追蹤")
                }
                else{
                    $('button[class="com_track"]').text("追蹤")
                }
                var commodity = result.commodity
                $('h3').text(result.com_name)
                $('span[class="price_"]').text(result.com_price)
                $('div[class="detail_picture"] img').attr('src',result.com_img)
                var html_=''
                for(var i=0;i<commodity.length;i++){
                    html_ +='<li class="mod_table">'
                    html_ +='<a target="_blank" href="'+commodity[i].mall_url+'">'
                    html_ +='<div>'
                    html_ +='<div class="mod_separetor">'
                    html_ +='<span class="botomlines">'+(Number(i)+1).toString()+'</span> '
                    html_ +='</div>'
                    html_ +='<div class="mod_name">'
                    html_ +='<span class="botomlines">'+commodity[i].mall_com_name+'</span>  '
                    html_ +='</div>'
                    html_ +='<div class="mod_price">'
                    html_ +='<span class="botomlines">$'+commodity[i].mall_price+'</span> '
                    html_ +='</div>'
                    html_ +='<div class="mall_name">'
                    html_ +='<span class="botomlines">'+commodity[i].mall_name+'</span>  '
                    html_ +='</div>'
                    html_ +='<div class="mod_go">'
                    html_ +='<span class="botomlines">點擊前往</span>  '
                    html_ +='</div></div></a></li>'                
                }
                $('ul[class="product_list"]').html(html_)
            }else{
             null
            }
        }
    })



})

function com_track(){
    var token = window.localStorage.getItem('Pricecompare_token');
    var username = window.localStorage.getItem('Pricecompare_user');
    var url = document.location.toString();    
    var arrUrl =url.split("//");
    var com_id= arrUrl[1].split('/')[2];
    var get_url = "http://127.0.0.1:8000/v1/detail/track"
    if (token == null | username == null){
        alert('尚未登入')
        window.location.href = '/'+'login';
    }else{
        var post_data = {'com_id':com_id};
        $.ajax({
            type:'put',
            url:get_url,
            dataType:'json',
            data:JSON.stringify(post_data),
            beforeSend: function(request) {      
            request.setRequestHeader("Authorization", token)
            },
            success:function(result){
                if(200 == result.code){       
                    if(1 == result.com_track){
                        $('button[class="com_track"]').text("取消追蹤")
                    }
                    else{
                        $('button[class="com_track"]').text("追蹤")
                    }
                }else if(107 == result.code){
                    alert('尚未登入')
                    window.location.href = '/'+'login';
                }
            }

        })
    }
    
}