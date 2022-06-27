const modalBtns = [...document.getElementsByClassName("modal-button")];
const modalBody = document.getElementById("modal-body-confirm");
const startBtn = document.getElementById("start-button");
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
    const time_Limit = modalBtn.getAttribute("data-time-limit");

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin <b>${topic}</b>?</div>
        <div class="text-muted">
            <ul>
                <li>start date: <b>${start_date}</b></li>
                <li>end date: <b>${end_date}</b></li>
                <li>number of attempts: <b>${number_of_attempts}</b></li>
                <li>Random: <b>${isRandom}</b></li>
                <li>Frequency: <b>${frequency}</b></li>
                <li>Time Limit: <b>${time_Limit} minutes</b></li>
            </ul>
        </div>
    `;

    // redirects to qb
    startBtn.addEventListener("click", () => {
      window.location.href = url + "question-banks/" + question_bank_id;
    });
  })
);
