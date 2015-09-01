
//获取在线人数和总人数
$(function(){

//   setInterval(get_users_count(), 0);
   $(document).ready(function(){
        get_users_count();
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
