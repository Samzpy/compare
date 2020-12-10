$(document).ready(function (){
    var get=$('.url').attr('href')
    var net='127.0.0.1:5000'
    $('.url').attr('href',get)
    });

function returnURL(){
    var net='127.0.0.1:5000';
    return net;
}