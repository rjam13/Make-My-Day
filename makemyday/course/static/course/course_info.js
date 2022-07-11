const modalBtns = [...document.getElementsByClassName("modal-button")];
const modalBody = document.getElementById("modal-body-confirm");
const startBtn = document.getElementById("start-button");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const url = window.location.href;

modalBtns.forEach((modalBtn) =>
    modalBtn.addEventListener("click", () => {
        const question_bank_id = modalBtn.getAttribute("data-pk");
        const topic = modalBtn.getAttribute("data-question-bank");
        const start_date = modalBtn.getAttribute("data-start-date");
        const end_date = modalBtn.getAttribute("data-end-date");
        const number_of_attempts = modalBtn.getAttribute("data-num-attempts");
        const isRandom = modalBtn.getAttribute("data-isRandom");
        const frequency = modalBtn.getAttribute("data-frequency");

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

        // Comments below is a possible approach to dealing with weekly notifications
        // html = `
        // <div class="h5 mb-3">Are you sure you want to begin <b>${topic}</b>?</div>
        // <div class="text-muted">
        //     <ul>
        //         <li>Start date: <b>${start_date}</b></li>
        //         <li>End date: <b>${end_date}</b></li>
        //         <li>Number of attempts per question: <b>${number_of_attempts}</b></li>
        //         <li>Frequency: <b>${frequency}</b></li>
        //     </ul>
        // `;
        // 
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
        // 
        // html += `
        // <p>Please enter a time to receive the questions <b>${frequency}</b>.</p>
        // <div id="error"></div>
        // <input type="time" id="noti" name="noti" required></input>
        // </div>
        // `;

        // const day_notification = document.getElementById("day");
        const form = document.getElementById("noti-form");
        const notification = document.getElementById("noti");
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

                $("[data-dismiss=modal]").trigger({ type: "click" });
            });
        });
    })
);
