const url = window.location.href;
const questionBox = document.getElementById("question-box");
const resultBox = document.getElementById("result-box");
const questionPrompt = document.getElementById("question-prompt");
const correctPrompt = document.getElementById("correct-prompt");
const explaPrompt = document.getElementById("explanation-prompt");
const answerPrompt = document.getElementById("answer-prompt");
const timerBox = document.getElementById("timer-box");
var theFormItself =  document.getElementById('question-form');
theFormItself.style.display = 'none';
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
        if (response.result) {
            showResults(response.result);
        } else {
            const data = response.data;
            const time_Limit = response.time_Limit;
            console.log(data);
            for (const [answer, explanation] of Object.entries(data)) {
                // {question: [answers in an array]} => [question, answers]
                theFormItself.style.display = 'block'
                questionBox.innerHTML += `
                <div>
                    <input type="radio" class="ans" id="${answer}" name="answers" value="${answer}">
                    <label for="${answer}">${answer}</label>
                </div>
                `;
            }
            activateTimer(time_Limit);
        }
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
        success: function (response) {
            // response == JsonResponse({'result': result}) from views.py
            showResults(response.result);
        },
        error: function (error) {
            console.log(error);
        },
    });
};

questionForm.addEventListener("submit", (e) => {
    e.preventDefault();
    clearInterval(timer);  
    theFormItself.style.display = 'none';
    sendData();
});

function showResults(result) { 
    const quesDiv = document.createElement("div");
    const corrDiv = document.createElement("div");
    const explDiv = document.createElement("div");
    const ansDiv = document.createElement("div");

    for (const [question, resp] of Object.entries(result)) {
        quesDiv.innerHTML += question;
        const cls = ["container", "p-3", "text-light", "h6"];
       
        const answer = resp["answered"];
        const correct = resp["correct_answer"];
        const explanation = resp["explanation"];
        corrDiv.innerHTML += correct;
        explDiv.innerHTML += explanation;
        ansDiv.innerHTML += "Correct!"
        if(answer != correct){
            ansDiv.innerHTML += answer;
        }
    }
    questionPrompt.append(quesDiv);
    correctPrompt.append(corrDiv);
    explaPrompt.append(explDiv);
    answerPrompt.append(ansDiv);
}