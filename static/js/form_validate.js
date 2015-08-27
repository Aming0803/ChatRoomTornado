function form_validate(){
    var user_name = $("#exampleInputEmail1").val();
    var user_pwd = $("#exampleInputPassword").val();
    var re_pwd = $("#repeatPassword").val();
    var phone = $("#phoneNum").val();
    if(!user_name){
        alert('请输入您的姓名！');
        return false;
    }
    if(!user_pwd){
        alert('请输入密码！');
        return false;
    }
    if(!re_pwd){
        alert('请输入确认密码！');
        return false;
    }
    if(user_pwd != re_pwd){
        alert('2次输入的密码不匹配！')
        return false;
    }
    if(!phone){
        alert('请输入您的联系方式！');
        return false;
    }

}