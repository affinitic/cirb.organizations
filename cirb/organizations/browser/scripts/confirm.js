$(document).ready(function() {
    $("#dialog").dialog({
        autoOpen: false,
        modal: true
    });

    $(".confirmDel").click(function(e) {
        e.preventDefault();
        var targetUrl = $(this).attr("href");

        $("#dialog").dialog({
            buttons : {
                          "Confirm" : function() {
                              window.location.href = targetUrl;
                          },
                            "Cancel" : function() {
                                $(this).dialog("close");
                          }
                      }
        });

        $("#dialog").dialog("open");
    });
});
