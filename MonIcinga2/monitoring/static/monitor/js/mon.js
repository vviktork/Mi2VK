setTimeout(
    function () {
      var url='ajax/';
      $.ajax({
          url: url,
          type: 'GET',
          data: {},
          success: function (html){
            $(document).ajaxStop(function(){
                window.location.reload();
                });
            $('#connect').html("Scaning");
            },
          error: function (){
            $('#connect').html("Error...");
            },
        });
    }, 60000);