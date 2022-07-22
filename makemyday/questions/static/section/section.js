const url = window.location.href;

// setting up the quiz from the corresponding section indicated in the URl
$.ajax({
    type: "GET",
    url: `${url}data`,
    success: function (response) {
        // questions is the array of questions with each value as {question: [info]}
        const past_questions = response.past_questions;
        const current_questions = response.current_questions;
        let buttonIDs = [];

        past_questions.forEach((element) => {
            for (const [question, info] of Object.entries(element)) {
                // {question: [info in an array]} => [question, info]

                document.getElementById("past-box").innerHTML += `
                        <div class="mb-2, container, p-3, text-light, h6,id="question${info["question_id"]}">
                        <button class="btn btn-link" style="text-decoration: none;" id="button${info["question_id"]}">${question}</button>
                        <p>Opened at ${info["open_datetime"].slice(0,16)}</p>

                    </div>
                `;
                buttonIDs.push(info["question_id"]);
            }
        });

        current_questions.forEach((element) => {
            for (const [question, info] of Object.entries(element)) {

                document.getElementById("today-box").innerHTML += `
                        <div class="mb-2, container, p-3, text-light, h6, id="question${info["question_id"]}">
                        <button class="btn btn-link" style="text-decoration: none;" id="button${info["question_id"]}">${question}</button>
                        <p>Opened today</p>
                    </div>
                `;

                buttonIDs.push(info["question_id"]);
            }
        });

        buttonIDs.forEach(function (buttonID) {
            $("#button" + buttonID).click(function () {
                window.location.href = url + buttonID;
            });
        });
    },
    error: function (error) {
        console.log(error);
    },
});