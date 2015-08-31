
//获取在线人数和总人数
   function get_users_count(){
       $.get(
            '/get_count',
            function(data){
                $(".contact-list").html(data);
                get_users_count();
            },
            'html'
       )
   }

