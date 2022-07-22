
const crButton = document.getElementById("cr-button");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const url = window.location.href;
const form = document.getElementById("cr-form");
const code = document.getElementById("cr-code");
const modalBody = document.getElementById("modal-body-confirm");

$(document).ready(function(){

    $('#cr-form').on('submit',function(e){
        e.preventDefault();
        access_code = String(code.value);

        $.ajax({
            type: "GET",
            url: `${url}course/get-course/`,
            data: {"access_code": access_code},
            success: function (response) {
                console.log(response);
                
                if(!response["error"]) {

                    const instructor = response["instructor"];
                    const course_id = response["course_id"];
                    const course_name = response["name"];
                    const description = response["description"];
                    const year = response["year"];
                    const semester = response["semester"];

                    modalBody.innerHTML = `
                    <div class="h5 mb-3">Are you sure you want to begin <b>${course_name}</b>?</div>
                    <div class="text-muted">
                        <ul>
                            <li>Course ID: <b>${course_id}</b></li>
                            <li>Instructor: <b>${instructor}</b></li>
                            <li>Year: <b>${year}</b></li>
                            <li>Semester: <b>${semester}</b></li>
                        </ul>
                        <p>${description}</p>
                        <p>Please enter a time to receive the questions <b>DAILY</b>.</p>
                        <input type="time" id="noti" name="noti" required>
                    </div>
                    `;

                    const notification = document.getElementById("noti");

                    // shows the modal
                    $('#courseStartModal').modal('show');

                    // The button for activating the question bank
                    $('#modal-body-confirm').ready(function(){

                        // for the modal close button
                        $('#modal-close-button').off('click');
                        $('#modal-close-button').on('click',function(e){
                            $('#courseStartModal').modal('hide');
                        });

                        // clears the submit event listeners, avoids multiple clicks required
                        $('#course-form').off('submit');

                        // add submit event listener
                        $('#course-form').on('submit',function(e){
                            e.preventDefault();
                            console.log(`signed up for ${course_name}`);

                            const data = {};
                            data["csrfmiddlewaretoken"] = csrf[0].value;
                            data["time"] = String(notification.value);
                            data["course_id"] = course_id

                            $.ajax({
                                type: "POST",
                                url: `${url}course/register/`,
                                data: data,
                                success: function (response) {
                                    console.log(response);
                                    if(response === "You are already signed up for this course.") {
                                        $('#courseStartModal').modal('hide');
                                    } else {
                                        window.location.reload()
                                    }
                                },
                                error: function (error) {
                                    console.log(error);
                                },
                            });
                        });
                    });
                } else {
                    console.log("Code is not Valid");
                }
            },
            error: function (error) {
                console.log(error);
            },
        });

    });
 
});

// The comments below are a possible approach to dealing with weekly notifications
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

