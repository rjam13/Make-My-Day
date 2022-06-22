const url = window.location.href;

// setting up the quiz from the corresponding question bank indicated in the URl
$.ajax({
  type: "GET",
  url: `${url}data`,
  success: function (response) {
    // questions is the array of questions with each value as {question: [info]}
    const questions = response.questions;
    // const responses = response.responses
    const time_Limit = response.time_Limit;
    let buttonIDs = []

    questions.forEach((element) => {
      for (const [question, info] of Object.entries(element)) {
        // {question: [info in an array]} => [question, info]

        color = ""
        if (info['answerIsCorrect'] == "True")
          color = "bg-success";
        else if (info['answerIsCorrect'] == "False")
          color = "bg-danger";

        const closedBox = document.getElementById("closed-box");
        const openBox = document.getElementById("open-box");
        const upcomingBox = document.getElementById("upcoming-box");
        const questionStatus = checkTimeInbetween(info['openDT'], info['closeDT']);

        html = `
            <hr>
            <div class="mb-2, container, p-3, text-light, h6, ${color}" id="question${info['question_id']}">
              <button class="btn btn-link" id="button${info['question_id']}">${question}</button>
        `;
        if (questionStatus == "open-box") {
          html += `
              <p>Open | Due: ${info['closeDT'].slice(0,16)} | Time: ${info['time_Limit']} minutes | ${info['weight']} pts</p>
          `;
        }
        else if (questionStatus == "upcoming-box") {
          html += `
              <p>Not available until ${info['openDT'].slice(0,16)} | Due: ${info['closeDT'].slice(0,16)} | Time: ${info['time_Limit']} minutes | ${info['weight']} pts</p>
          `;
        }
        else if (questionStatus == "closed-box") {
          html += `
              <p>Closed | Due: ${info['closeDT'].slice(0,16)} | ${info['weight']} pts</p>
          `;
        }
        html += `</div>`;

        if (questionStatus == "open-box") {
          openBox.innerHTML += html;
        }
        else if (questionStatus == "upcoming-box") {
          upcomingBox.innerHTML += html;
        }
        else if (questionStatus == "closed-box") {
          closedBox.innerHTML += html;
        }

        buttonIDs.push(info['question_id']);
      }
    });

    buttonIDs.forEach(function(buttonID) {
      $("#button"+buttonID).click(function() {
        window.location.href = url + buttonID;
      });
    });
  },
  error: function (error) {
    console.log(error);
  },
});

function checkTimeInbetween(openDT, closeDT) {
  const beg = Date.parse(openDT);
  const now = Date.parse(new Date());
  const end = Date.parse(closeDT);

  if (beg < now && now < end) {
    return "open-box";
  } else if (now < beg) {
    return "upcoming-box";
  } else {
    return "closed-box";
  }

}
