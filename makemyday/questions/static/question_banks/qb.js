console.log("hello world");

const url = window.location.href;
const qbBox = document.getElementById("qb-box");

// setting up the quiz from the corresponding question bank indicated in the URl
$.ajax({
  type: "GET",
  url: `${url}data`,
  success: function (response) {
    // data is the array of questions with each value as a dictionary = {question: answers in an array}
    const data = response.data;
    data.forEach((element) => {
      for (const [question, answers] of Object.entries(element)) {
        // {question: answers in an array} => [question, answers]
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

const qbForm = document.getElementById("qb-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

// called when the submit button is pressed
const sendData = () => {
  const elements = [...document.getElementsByClassName("ans")]; // contains all the radio buttons
  const data = {};
  data["csrfmiddlewaretoken"] = csrf[0].value;
  // go through all the possible answers
  elements.forEach((el) => {
    if (el.checked) {
      // name = question
      // value = answer
      data[el.name] = el.value;
    } else {
      // if question has no entry in data, it was not answered.
      if (!data[el.name]) {
        data[el.name] = null;
      }
    }
  });

  // calls save_qb_view function in views.py
  $.ajax({
    type: "POST",
    url: `${url}save/`,
    data: data, // data == request.POST
    success: function (response) {
      console.log(response);
    },
    error: function (error) {
      console.log(error);
    },
  });
};

qbForm.addEventListener("submit", (e) => {
  e.preventDefault();

  sendData();
});
