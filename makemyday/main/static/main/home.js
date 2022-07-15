const crButton = document.getElementById("cr-button");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const url = window.location.href;
const form = document.getElementById("cr-form");
const code = document.getElementById("cr-code");

$(document).ready(function(){

    $('#cr-form').on('submit',function(e){
        e.preventDefault();
        const data = {};
        data["csrfmiddlewaretoken"] = csrf[0].value;
        data["code"] = String(code.value);

        $.ajax({
            type: "POST",
            url: `${url}course/register/`,
            data: data,
            success: function (response) {
                window.location.href = url
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            },
        });

    });
 
});

