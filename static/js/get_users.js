
//获取在线人数和总人数;
//多人聊天
$(function(){

    //获取聊天人数
    get_users_count();
    //更新聊天记录
    message_update();
    //发送消息

    $("#messageform").on("click", function() {
        var message = $("#message").val();
        if(message){
          newMessage(message);
        }else{
          alert("消息不能为空");
        }

        return false;
    });

    $("#messageform").on("keypress", function(e) {
        var message = $("#message").val();
        if(message){
          if (e.keyCode == 13) {
            newMessage(message);
            }
        }else{
          alert("消息不能为空");
        }
        return false;
    })
})

function get_users_count(){
        $.ajax({
            type:'GET',
            url:'/get_count',
            dataType:'html',
            success:function(data, textStatus){
                $(".contact-list").html(data);
                if (textStatus == "success") { // 请求成功
                    setInterval(get_users_count(), 0);
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                setInterval(get_users_count(),500);
            }
        })
   }


function message_update(){
    $.ajax({
            type:'GET',
            url:'/message/update',
            dataType:'html',
            success:function(data, textStatus){
                $("#message_box").append(data);
                if (textStatus == "success") { // 请求成功
                    setInterval(message_update(), 0);
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                setInterval(message_update(),500);
            }
        })
}

function newMessage(message){
    var xsrf = getCookie("_xsrf");
    $.post(
        '/message/new',
        {'message':message, '_xsrf':xsrf},
        function(response){
            $("#messgae").val("");
        }
    )
}

function MessageRealTimePush(){
    $.ajax({
            type:'GET',
            url:'/message/update',
            dataType:'html',
            success:function(data, textStatus){
                $("#message_box").append(data);
                if (textStatus == "success") { // 请求成功
                    setInterval(message_update(), 0);
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                setInterval(message_update(),500);
            }
        })
}