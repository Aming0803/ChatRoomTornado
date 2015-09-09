$(function(){
//一对一聊天
    $("#messageform").on("click", function() {
        var message = $("#message").val();
        if(message){
            newMessage();
        }else{alert("不能为空")}

        return false;
    });
    $("#messageform").on("keypress", function(e) {
        var message = $("#message").val();
        if(message){
            if (e.keyCode == 13) {
                newMessage();
            }
        }else{alert("不能为空")}
        return false;
    });
    updater.start();
})

function newMessage() {
    var message = {
        'info':$("#message").val()
    }
    updater.socket.send(JSON.stringify(message));
    $("#message").val("");
}

var updater = {
    socket: null,

    start: function() {
        to_user_id = $("#other_user").val();
        cur_user = $("#cur_user").val();
        var url = "ws://" + location.host + "/websocket/single?to_user_id="+to_user_id;
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            var response = JSON.parse(event.data)
            var li;
            if(response.user != cur_user){
                li = $('<li></li>');
            }else{
                var li = $('<li class="current-user"></li>');
            }
            li.html($(response.html));
            $("#message_box").append(li);
        }
    },
};