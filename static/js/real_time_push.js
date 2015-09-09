$(function(){
    MessageRealTimePush();
})



function MessageRealTimePush(){
    $.ajax({
            type:'GET',
            url:'/message/push',
            dataType:'html',
            success:function(data, textStatus){
                if (textStatus == "success") { // 请求成功
                    $("#new_message").html(data);
                    $("#message_push").slideDown();
                    $("#delete").click(function(){
                        $("#message_push").slideUp();
                    });
                    setInterval(MessageRealTimePush(), 0);
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                setInterval(MessageRealTimePush(),500);
            }
        })
}
