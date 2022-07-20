const url = window.location.href;
const questionBox = document.getElementById("question-box");
const resultBox = document.getElementById("result-box");
const questionPrompt = document.getElementById("question-prompt");
const correctPrompt = document.getElementById("correct-prompt");
const explaPrompt = document.getElementById("explanation-prompt");
const answerPrompt = document.getElementById("answer-prompt");
const feedbackSymbol = document.getElementById("feedback-symbol")
const timerBox = document.getElementById("timer-box");
var corrAnsDiv = document.getElementById("corr-ans")
var yourAnsDiv = document.getElementById("your-ans");
var theFormItself =  document.getElementById('question-form');
corrAnsDiv.style.display = 'none'
yourAnsDiv.style.display = 'none'
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
<<<<<<< HEAD
    clearInterval(timer);  
=======
    clearInterval(timer);
>>>>>>> main
    theFormItself.style.display = 'none';
    sendData();
});

<<<<<<< HEAD
function showResults(result) { 
=======
function showResults(result) {
>>>>>>> main
    const quesDiv = document.createElement("div");
    const corrDiv = document.createElement("div");
    const explDiv = document.createElement("div");
    const ansDiv = document.createElement("div");
    const feedbackSymbolDiv = document.createElement("div")

    for (const [question, resp] of Object.entries(result)) {
        quesDiv.innerHTML += question;
        const cls = ["container", "p-3", "text-light", "h6"];
<<<<<<< HEAD
       
=======

>>>>>>> main
        const answer = resp["answered"];
        const correct = ": " + resp["correct_answer"];
        const explanation = resp["explanation"];
        corrDiv.innerHTML += correct;
        explDiv.innerHTML += explanation;

        if(": " + answer != correct){ // If answer is
            feedbackSymbolDiv.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" style="position:relative; float:left; left:60px; margin-right:8px; color:red; margin-top:4px" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
            </svg>
            `
            ansDiv.innerHTML += ": " + answer;
        }else{
            feedbackSymbolDiv.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" style="position:relative; float:left; left:60px; margin-right:8px; color:green; margin-top:4px" width="16" height="16" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
            </svg>
            `
            ansDiv.innerHTML += "&nbspCorrectly!"

        }
    }
    corrAnsDiv.style.display = 'block'
    yourAnsDiv.style.display = 'block'
    questionPrompt.append(quesDiv);
    correctPrompt.append(corrDiv);
    explaPrompt.append(explDiv);
    answerPrompt.append(ansDiv);
    feedbackSymbol.append(feedbackSymbolDiv);
}

