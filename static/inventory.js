$(document).ready(function() {
    // setTimeout(requestInventory, 100);
    $('#add-button').click(function(){
        var xsrf = getCookie("_xsrf");
        // data._xsrf = getCookie("_xsrf");
        $.ajax({
            // cache:false,
            url: "/mqtt",
            type: 'post',
            headers: {
                   "X-XSRFToken":xsrf,
                    },
            data: {
                // session: document.data,
                // action: 'add',
                send_data: document.getElementById("send_data").value,
                // data: jQuery.param(data),
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                    // alert(document.getElementById("send_data").value);
                // $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                alert('success');
                // $('#add-to-cart').hide();
                // $('#remove-from-cart').show();
                // $(event.target).removeAttr('disabled');
            }
        });
    });

    // $('#remove-button').click(function(event) {
    //     jQuery.ajax({
    //         url: '127.0.0.1:8888/cart',
    //         type: 'POST',
    //         data: {
    //             session: document.session,
    //             action: 'remove'
    //         },
    //         dataType: 'json',
    //         beforeSend: function(xhr, settings) {
    //             $(event.target).attr('disabled', 'disabled');
    //         },
    //         success: function(data, status, xhr) {
    //             $('#remove-from-cart').hide();
    //             $('#add-to-cart').show();
    //             $(event.target).removeAttr('disabled');
    //         }
    //     });
    // });
});
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}
// function requestInventory() {
//     jQuery.getJSON('127.0.0.1:8888/cart/status', {session: document.session},
//         function(data, status, xhr) {
//             $('#count').html(data['inventoryCount']);
//             setTimeout(requestInventory, 0);
//         }
//     );
// }