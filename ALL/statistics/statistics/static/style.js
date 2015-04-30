$(document).ready(function(){
  $('#button').click(function(){
      value=$('#content').val();
      window.location='/log/search/'+value+'/';    
     }); 
});    
