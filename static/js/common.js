$(function(){
//关于checkbox选择问题
   $(".face input").click(function(){
      ($(".face input").not($(this))).prop('checked', false);
   });
   $(".sex input").click(function(){
      ($(".sex input").not($(this))).prop('checked', false);
   })
})