const url = window.location.href;

// setting up the quiz from the corresponding question bank indicated in the URl
$.ajax({
    type: "GET",
    url: `${url}data`,
    success: function (response) {
        // questions is the array of questions with each value as {question: [info]}
        const closed_qs = response.closed_qs;
        const open_qs = response.open_qs;
        const upcoming_qs = response.upcoming_qs;
        // const responses = response.responses
        let buttonIDs = [];

        closed_qs.forEach((element) => {
            for (const [question, info] of Object.entries(element)) {
                // {question: [info in an array]} => [question, info]

                color = "";
                if (info["answerIsCorrect"] == "True") 
                    color = "bg-success";
                else if (info["answerIsCorrect"] == "False")
                    color = "bg-danger";

                document.getElementById("closed-box").innerHTML += `
                    <hr>
                        <div class="mb-2, container, p-3, text-light, h6, ${color}" id="question${info["question_id"]}">
                        <button class="btn btn-link" id="button${info["question_id"]}">${question}</button>
                        <p>Closed | Due: ${info["closeDT"].slice(0, 16)} | ${info["weight"]} pts</p>
                    </div>
                `;

                buttonIDs.push(info["question_id"]);
            }
        });

        open_qs.forEach((element) => {
            for (const [question, info] of Object.entries(element)) {

                color = "";
                if (info["answerIsCorrect"] == "True") 
                    color = "bg-success";
                else if (info["answerIsCorrect"] == "False")
                    color = "bg-danger";

                document.getElementById("open-box").innerHTML += `
                    <hr>
                        <div class="mb-2, container, p-3, text-light, h6, ${color}" id="question${info["question_id"]}">
                        <button class="btn btn-link" id="button${info["question_id"]}">${question}</button>
                        <p>Open | Due: ${info["closeDT"].slice(0, 16)} | Time: ${info["time_Limit"]} minutes | ${info["weight"]} pts</p>
                    </div>
                `;

                buttonIDs.push(info["question_id"]);
            }
        });

        upcoming_qs.forEach((element) => {
            for (const [question, info] of Object.entries(element)) {

                color = "";
                if (info["answerIsCorrect"] == "True") 
                    color = "bg-success";
                else if (info["answerIsCorrect"] == "False")
                    color = "bg-danger";

                document.getElementById("upcoming-box").innerHTML += `
                    <hr>
                        <div class="mb-2, container, p-3, text-light, h6, ${color}" id="question${info["question_id"]}">
                        <a>${question}</a>
                        <p>Not available until ${info["openDT"].slice(0,16)} | Due: ${info["closeDT"].slice(0, 16)} | Time: ${info["time_Limit"]} minutes | ${info["weight"]} pts</p>
                    </div>
                `;

                // document.getElementById("upcoming-box").innerHTML += `
                //     <hr>
                //         <div class="mb-2, container, p-3, text-light, h6, ${color}" id="question${info["question_id"]}">
                //         <button class="btn btn-link" id="button${info["question_id"]}">${question}</button>
                //         <p>Not available until ${info["openDT"].slice(0,16)} | Due: ${info["closeDT"].slice(0, 16)} | Time: ${info["time_Limit"]} minutes | ${info["weight"]} pts</p>
                //     </div>
                // `;

                // buttonIDs.push(info["question_id"]);
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
