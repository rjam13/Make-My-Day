console.log("hello world");

const url = window.location.href;
const qbBox = document.getElementById("qb-box");

$.ajax({
  type: "GET",
  url: `${url}data`,
  success: function (response) {
    const data = response.data;
    data.forEach((element) => {
      for (const [question, answers] of Object.entries(element)) {
        qbBox.innerHTML += `
            <hr>
            <div class="mb-2">
                <b>${question}</b>
            </div>
        `;
        answers.forEach((answer) => {
          qbBox.innerHTML += `
                <div>
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for="${question}">${answer}</label>
                </div>
            `;
        });
      }
    });
  },
  error: function (error) {
    console.log(error);
  },
});
