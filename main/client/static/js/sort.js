var arrData=[
    {  'mobile':{
        lt:'手機',
        lu:'所有手機',
        b:{
            "apple":'APPLE 蘋果',
            'samsung':'SAMSUNG 三星',
            'vivo':'VIVO 維沃',
            'sony':'SONY 索尼',
        },

    }},
    { 'tv':{
        lt:'電視',
        lu:'所有電視',
        b:{
            'chimei':'CHIMEI 奇美',
            'samsung':'SAMSUNG 三星',
            'philips':'PHILIPS 飛利浦',
            'sony':'SONY 索尼',
            'panasonic':'Panasonic 國際牌',
        }
    }},
    { 'sound':{
        lt:'音響',
        lu:'所有音響',
        b:{
            'bose':'BOSE',
            'edifer':'EDIFER',
            'logitech':'LOGITECH',
            'sony':'SONY 索尼',
            'jbl':'JBL',
        }
    }},
    { 'fan':{
        lt:'電扇',
        lu:'所有電扇',
        b:{
            'kolin':'Kolin 歌林',
            'panasonic':'PANASONIC 國際牌',
            'samlux':'SAMLUX 三洋',
            'wind':'勳風',
            'teco':'TECO 東元',
        }
    }},
    { 'refrigerator':{
        lt:'冰箱',
        lu:'所有冰箱',
        b:{
            'lg':'LG 樂金',
            'panasonic':'PANASONIC 國際牌',
            'samlux':'SAMLUX 三洋',
            'sharp':'SHARP 夏普',
            'toshiba':'TOSHIBA 東芝',
        }
    }},
    { 'conditioningmachine':{
        lt:'調理機',
        lu:'所有調理機',
        b:{
            'blendtec':'Blendtec',
            'cuisinart':'Cuisinart',
            'joyoung':'Joyoung 九陽',
            'kitchenaid':'KitchenAid',
            'vitamix':'Vita-Mix',
        }
    }},
    { 'hairdryer':{
        lt:'吹風機',
        lu:'所有吹風機',
        b:{
            'kinyo':'KINYO 耐嘉',
            'panasonic':'PANASONIC 國際牌',
            'philips':'PHILIPS 飛利浦',
            'tescom':'TESCOM',
            'zushiang':'ZUSHIANG 日象',
        }
    }},
    { 'razor':{
        lt:'刮鬍刀',
        lu:'所有刮鬍刀',
        b:{
            'kinyo':'KINYO 耐嘉',
            'panasonic':'PANASONIC 國際牌',
            'philips':'PHILIPS 飛利浦',
            'kolin':'Kolin 歌林',
            'zushiang':'ZUSHIANG 日象',
        }
    }},
    { 'oven':{
        lt:'烤箱',
        lu:'所有烤箱',
        b:{
            'heran':'HERAN 禾聯',
            'panasonic':'PANASONIC 國際牌',
            'tatung':'TATUNG 大同',
            'whirlpool':'WHIRLPOOL 惠而浦',
            'yamasaki':'Yamasaki 山崎',
        }
    }}
 ]

$(document).ready(function (){
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var sort = arrUrl[1].split('/')[2].split('?')[0];
    var bord = arrUrl[1].split('/')[2].split('?')[1].split('=')[1].split('&')[0];

    for(var i=0;i<arrData.length;i++){
        var html_=''
        // arrData 大標 mobile
        var key=Object.keys(arrData[i])[0]
        if (sort == key & bord=="all"){
            // ["apple", "samsung", "vivo", "sony"]
            var key_b=Object.keys(arrData[i][sort]['b'])
            // {apple: "APPLE 蘋果", samsung: "SAMSUNG 三星", vivo: "VIVO 維沃", sony: "SONY 索尼"}
            var singleDict = arrData[i][sort]['b']
            $('.phonetitle').text(arrData[i][key]['lt']);
            $('.indexleft').text(arrData[i][key]['lu']);
            html_ += '<a href="http://127.0.0.1:5000/sort/' + key + '?brand=all"  class ="list-group-item list-group-item-action phonedetail">所有 </a>'
            for(var b=0;b < key_b.length ; b++){
                html_ += '<a href="http://127.0.0.1:5000/sort/' + key+ '?brand='+ key_b[b]+'" class="list-group-item list-group-item-action phonedetail">'+singleDict[key_b[b]]+' </a>'
            }      

            $('.leftlist').html(html_)               
        }
        else if(sort==key & bord !="all"){
            // ["apple", "samsung", "vivo", "sony"]
            var key_b=Object.keys(arrData[i][sort]['b'])
            // {apple: "APPLE 蘋果", samsung: "SAMSUNG 三星", vivo: "VIVO 維沃", sony: "SONY 索尼"}
            var singleDict = arrData[i][sort]['b']
            $('.phonetitle').text(arrData[i][key]['lt']);       
            var html_=''
            html_ += '<a href="http://127.0.0.1:5000/sort/' + key + '?brand=all"  class ="list-group-item list-group-item-action phonedetail">所有 </a>'
            for(var b=0;b<key_b.length;b++){
                html_ += '<a href="http://127.0.0.1:5000/sort/' + key+ '?brand='+ key_b[b]+'" class="list-group-item list-group-item-action phonedetail">'+singleDict[key_b[b]]+' </a>'
                if(bord == key_b[b]){
                    $('.indexleft').text(singleDict[key_b[b]]);
                }
            }
            $('.leftlist').html(html_)    
        }
     } 
    }
    )





