$(document).ready(function() {
    $('#add-button').click(function(){
        var xsrf = getCookie("_xsrf");
        $.ajax({
            url: "/mqtt",
            type: 'post',
            headers: {
                   "X-XSRFToken":xsrf,
                    },
            data: {
                send_data: document.getElementById("send_data").value,
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
            },
            success: function(data, status, xhr) {
                alert('success');

            }
        });
    });

});
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}

$(document).ready(function() {
    $('#send-button').click(function(){
        var xsrf = getCookie("_xsrf");
        $.ajax({
            url: "/wifi",
            type: 'post',
            headers: {
                   "X-XSRFToken":xsrf,
                    },
            data: {
                send_data: document.getElementById("wifi_data").value,
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
            },
            success: function(data) {
                alert(data.message);
            }
        });
    });

});
