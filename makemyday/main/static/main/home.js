const crButton = document.getElementById("cr-button");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const url = window.location.href;
const form = document.getElementById("cr-form");
const code = document.getElementById("cr-code");

form.addEventListener("submit", (e) => {
    e.preventDefault();

    crButton.addEventListener("click", () => {
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

// $("#cr-form").on("click", () => {
//     let messages = [];
//     if (code.value === "" || code.value === null) {
//         messages.push("Code is required");
//     }
//     if (messages.length > 0) {
//         errorElement.innerHTML = messages.join(", ");
//     }

//     $("#cr-button").click(() => {
//         const data = {};
//         data["csrfmiddlewaretoken"] = csrf[0].value;
//         data["code"] = String(code.value);
    
//         $.ajax({
//             type: "POST",
//             url: `${url}course/register/`,
//             data: data,
//             success: function (response) {
//                 window.location.href = url
//                 console.log(response);
//             },
//             error: function (error) {
//                 console.log(error);
//             },
//         });
//     });
    
// });

