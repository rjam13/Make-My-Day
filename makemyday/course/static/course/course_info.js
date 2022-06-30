const modalBtns = [...document.getElementsByClassName("modal-button")];
const modalBody = document.getElementById("modal-body-confirm");
const startBtn = document.getElementById("start-button");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const url = window.location.href;

modalBtns.forEach((modalBtn) =>
    modalBtn.addEventListener("click", () => {
        // retrieve all the attributes set to the button by django
        // views.py:QuestionBankListView(ListView) -> main_qb.html -> here
        const question_bank_id = modalBtn.getAttribute("data-pk");
        const topic = modalBtn.getAttribute("data-question-bank");
        const start_date = modalBtn.getAttribute("data-start-date");
        const end_date = modalBtn.getAttribute("data-end-date");
        const number_of_attempts = modalBtn.getAttribute("data-num-attempts");
        const isRandom = modalBtn.getAttribute("data-isRandom");
        const frequency = modalBtn.getAttribute("data-frequency");

        // $.ajax({
        //   type: "GET",
        //   url: `${url}data`,
        //   success: function (response) {
        //     const questions = response.questions;
        //     const time_Limit = response.time_Limit;
        //     let buttonIDs = []

        //     questions.forEach((element) => {
        //       for (const [question, info] of Object.entries(element)) {

        //         color = ""
        //         if (info['answerIsCorrect'] == "True")
        //           color = "bg-success";
        //         else if (info['answerIsCorrect'] == "False")
        //           color = "bg-danger";

        //       }
        //     });
        //   },
        //   error: function (error) {
        //     console.log(error);
        //   },
        // });

        modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin <b>${topic}</b>?</div>
        <div class="text-muted">
            <ul>
                <li>Start date: <b>${start_date}</b></li>
                <li>End date: <b>${end_date}</b></li>
                <li>Number of attempts per question: <b>${number_of_attempts}</b></li>
                <li>Frequency: <b>${frequency}</b></li>
            </ul>
            <p>Please enter a time to receive the questions <b>${frequency}</b>.</p>
            <div id="error"></div>
            <input type="time" id="noti" name="noti" required>
        </div>
        `;

        html = `
        <div class="h5 mb-3">Are you sure you want to begin <b>${topic}</b>?</div>
        <div class="text-muted">
            <ul>
                <li>Start date: <b>${start_date}</b></li>
                <li>End date: <b>${end_date}</b></li>
                <li>Number of attempts per question: <b>${number_of_attempts}</b></li>
                <li>Frequency: <b>${frequency}</b></li>
            </ul>
        `;

        // if (frequency == "WEEKLY") {
        //   html += `
        //   <p>Please enter a day and time to receive the questions <b>${frequency}</b>.</p>
        //   <div id="error"></div>
        //   <select name="day" id="day" required>
        //       <option value="sunday">Sunday</option>
        //       <option value="monday">Monday</option>
        //       <option value="tuesday">Tuesday</option>
        //       <option value="wednesday">Wednesday</option>
        //       <option value="thursday">Thursday</option>
        //       <option value="friday">Friday</option>
        //       <option value="saturday">Saturday</option>
        //   </select>
        //   <input type="time" id="noti" name="noti" required>
        //   `
        // } else {
        //   html += `
        //   <p>Please enter a time to receive the questions <b>${frequency}</b>.</p>
        //       <div id="error"></div>
        //       <input type="time" id="noti" name="noti" required></input>
        //   `
        // }

        html += `
        <p>Please enter a time to receive the questions <b>${frequency}</b>.</p>
        <div id="error"></div>
        <input type="time" id="noti" name="noti" required></input>
        </div>
        `;

        const form = document.getElementById("noti-form");
        const notification = document.getElementById("noti");
        // const day_notification = document.getElementById("day");
        const errorElement = document.getElementById("error");

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            let messages = [];
            if (notification.value === "" || notification.value === null) {
                messages.push("Time for notification is required");
            }
            if (messages.length > 0) {
                errorElement.innerHTML = messages.join(", ");
            }

            startBtn.addEventListener("click", () => {
                const data = {};
                data["csrfmiddlewaretoken"] = csrf[0].value;
                data["time"] = String(notification.value);

                $.ajax({
                    type: "POST",
                    url: `${url}question-banks/${question_bank_id}/activate-qb/`,
                    data: data,
                    success: function (response) {
                        console.log(response);
                    },
                    error: function (error) {
                        console.log(error);
                    },
                });

                // goes back to the homepage
                // window.location.href = url + "question-banks/" + question_bank_id;
                $("[data-dismiss=modal]").trigger({ type: "click" });
            });
        });
    })
);
