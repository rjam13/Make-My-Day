const url = window.location.href;
const questionBox = document.getElementById("question-box");
const resultBox = document.getElementById("result-box");
const timerBox = document.getElementById("timer-box");
var timer;

const activateTimer = (time) => {
  if (time.toString().length < 2) {
    timerBox.innerHTML = `<b>0${time}:00</b>`;
  } else {
    timerBox.innerHTML = `<b>${time}:00</b>`;
  }

  let minutes = time - 1;
  let seconds = 60;
  let displaySeconds;
  let displayMinutes;

  timer = setInterval(() => {
    seconds--;
    if (seconds < 0) {
      seconds = 59;
      minutes--;
    }
    if (minutes.toString().length < 2) {
      displayMinutes = "0" + minutes;
    } else {
      displayMinutes = minutes;
    }

    if (seconds.toString().length < 2) {
      displaySeconds = "0" + seconds;
    } else {
      displaySeconds = seconds;
    }

    if (minutes == 0 && seconds == 0) {
      timerBox.innerHTML = "<b>00:00</b>";
      setTimeout(() => {
        clearInterval(timer);
        alert("time over");
        sendData();
      }, 500);
    }

    timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
  }, 1000);
};

// setting up the question from the corresponding question bank indicated in the URl
$.ajax({
  type: "GET",
  url: `${url}data`,
  success: function (response) {
    // data is the array of questions with each value as {question: [answers in an array]}
    const data = response.data;
    const time_Limit = response.time_Limit;
    console.log(data);
    for (const [answer, explanation] of Object.entries(data)) {
      // {question: [answers in an array]} => [question, answers]
      questionBox.innerHTML += `
            <div>
                <input type="radio" class="ans" id="${answer}" name="answers" value="${answer}">
                <label for="${answer}">${answer}</label>
            </div>
        `;
    };
    activateTimer(time_Limit);
  },
  error: function (error) {
    console.log(error);
  },
});

const questionForm = document.getElementById("question-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

// called when the submit button is pressed
const sendData = () => {
  const elements = [...document.getElementsByClassName("ans")]; // contains all the radio buttons
  const data = {};
  const questionText = document.getElementById("question").innerHTML;
  data["csrfmiddlewaretoken"] = csrf[0].value;
  // go through all the possible answers
  elements.forEach((el) => {
    if (el.checked) {
      // name = question
      // value = answer
      data[questionText] = el.value;
    } else if (!data[questionText]) {
      // if question has no entry in data, it was not answered.
      data[questionText] = null;
    }
  });

  // calls save_question_view function in views.py
  $.ajax({
    type: "POST",
    url: `${url}save/`,
    data: data, // data == request.POST in save_question_view in views.py
    success: function (response) { // response == JsonResponse({'result': result}) from views.py
      // displays all the results
      const result = response.result;
      questionForm.classList.add("invisible");

      // scoreBox.innerHTML = `Your result is ${response.score.toFixed(2)}%`;

      // results.forEach((res) => {
      // {str(q): {'correct_answer': correct_answer, 'answered': a_selected}} => [question, resp]
      // {str(q): 'not answered'} => [question, resp]
      const resDiv = document.createElement("div");
      for (const [question, resp] of Object.entries(result)) {

        resDiv.innerHTML += question;
        const cls = ["container", "p-3", "text-light", "h6"];
        resDiv.classList.add(...cls);

        if (resp == "not answered") {
          resDiv.innerHTML += "- not answered";
          resDiv.classList.add("bg-danger");
        } else {
          const answer = resp["answered"];
          const correct = resp["correct_answer"];

          if (answer == correct) {
            resDiv.classList.add("bg-success");
            resDiv.innerHTML += `answered: ${answer}`;
          } else {
            resDiv.classList.add("bg-danger");
            resDiv.innerHTML += ` | correct answer: ${correct}`;
            resDiv.innerHTML += ` | answered: ${answer}`;
          }
        }
      }
      resultBox.append(resDiv);
      // });
    },
    error: function (error) {
      console.log(error);
    },
  });
};

questionForm.addEventListener("submit", (e) => {
  e.preventDefault();
  clearInterval(timer);
  sendData();
});
