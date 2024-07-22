function loadQuestion() {
    if (document.getElementById("solution_image")) {
        document.getElementById("solution_image").remove();
    }

    question = data[q_counter];

    const [q, c] = Object.entries(question)[0]; // Object.entries() turns dictionaries/hashmaps to enumerated arrays
    document.getElementById("question").innerHTML = q;
    document.getElementById("choices").innerHTML = '';

    c.forEach(choice =>{
        document.getElementById("choices").innerHTML += `
            <div>
                <input type="radio" class="choice" id="${q} ${choice}" name="${q}" value="${choice}">
                <label for="${q}">${choice}</label>
            </div>
        `;
    });

    form = document.getElementById("multiple_choice");
    csrf = document.getElementsByName("csrfmiddlewaretoken");
    elements = [...document.getElementsByClassName("choice")];
    view_solution_button = document.getElementById("solution_button");

    document.getElementById("submit_button").innerHTML = "Answer!";
    view_solution_button.style.display = "none";
}

function getFormInputs() {    
    var data = {};

    data["csrfmiddlewaretoken"] = csrf[0].value;

    elements.forEach(element => {
        if (element.checked) {
            data[element.name] = element.value;
        }
    });

    if (!data[elements[0].name]) {
        data[elements[0].name] = null;
    }

    $.ajax({
        method: "POST",
        url: `${url}/check-answer`,
        data: data,
        success: function(response) {
            submit_counter++;

            if (response.status == true) {
                correct_counter++;
                var myModal = new bootstrap.Modal(document.getElementById("correctModal"), {});
            } else {
                document.getElementById("incorrectMessage").innerHTML = `The correct answer should be ${response.correct_answer}`;
                var myModal = new bootstrap.Modal(document.getElementById("wrongModal"), {});
            }
            q_counter++;
            if (q_counter < parseInt(t_question)) {
                progress += parseInt(1/t_question * 100);
                document.getElementById("submit_button").innerHTML = "Next Question";
            } else {
                progress = 100;
                document.getElementById("submit_button").innerHTML = "Results";
            }
            progress_bar.setAttribute("aria-valuenow", `${progress}`);
            progress_bar.children[0].setAttribute("style", `width: ${progress}%`);

            myModal.toggle();
        },
        error: function(error) {
            console.Log(error);
        }
    });
}

function Results() {
    form.remove();

    const user_score = parseInt(correct_counter / parseInt(t_question) * 100);
    var color;
    var final_message;
    var try_again = "";

    if (user_score >= parseInt(quiz_passing)) {
        color = "text-success";
        final_message = "You Passed!!!!🥳";
    } else {
        color = "text-danger";
        final_message = "You Failed!😞";
        try_again ="Try it again..."
    }

    document.getElementById("regUserContent").innerHTML = `
        <table class="table text-dark text-center fw-bold mt-3">
            <thead>
                <tr>
                    <th scope="col">Quiz Unit</th>
                    <th scope="col">Number of Questions</th>
                    <th scope="col">Mark to Pass</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${quiz_unit}</td>
                    <td>${t_question}</td>
                    <td>${quiz_passing}%</td>
                </tr>
            </tbody>
        </table>
        <h2 class="text-center mt-5 fw-bold display-4" id="percentage">
            You Got: <span class="${color}">
                        ${user_score}%
                        <br>
                        ${final_message}
                     </span>
        </h2>
        <h4 class="text-center">
            ${try_again}
        </h4>
    `;
}

function getSolution() {
    var data = {};
    const [q, c] = Object.entries(question)[0];

    data["csrfmiddlewaretoken"] = csrf[0].value;
    data["question_name"] = q;

    $.ajax({
        method: "POST",
        url: `${url}/show-answer`,
        data: data,
        success: function(response) {
            document.getElementById("regUserContent").innerHTML += `
                <div class="border-top border-2 border-dark mt-5 text-center p-3" id="solution_image">
                    <img src="data:image/png;base64,${response["image"]}" class="card-img-top" alt="${q} solution" style="height: 100%; width: 100%;">
                </div>
            `;
            form = document.getElementById("multiple_choice");
            view_solution_button = document.getElementById("solution_button");

            formEvent();
            solutionEvent();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function formHandler(e) {
    e.preventDefault();
    
    if (q_counter < parseInt(t_question)) {
        if (submit_counter == 0) {
            getFormInputs();
            view_solution_button.style.display = "block";
        } else {
            submit_counter = 0;
            loadQuestion();
        }
    } else {
        Results();
    }
}

function solutionHandler(e) {
    e.preventDefault();
    view_solution_button.style.display = "none";

    getSolution();
}

function formEvent() {
    if (!formEventListener) {
        form.addEventListener("submit", formHandler);
        formEventListener = true;
    } else {
        form.removeEventListener("submit", formHandler);
        form.addEventListener("submit", formHandler);
    }
}

function solutionEvent() {
    if (!solutionEventListener) {
        view_solution_button.addEventListener("click", solutionHandler);
        solutionEventListener = true;
    } else {
        view_solution_button.removeEventListener("click", solutionHandler);
        view_solution_button.addEventListener("click", solutionHandler);
    }  
}
// console.log(data); //print statement

var question;
var q_counter = 0;
var form;
var csrf;
var elements;
var view_solution_button;
var formEventListener = false;
var solutionEventListener = false;
var submit_counter = 0;
var correct_counter = 0;
var progress_bar = document.getElementById("progressbar");
var progress = 0;
const url = window.location.href;
// console.log(url);

loadQuestion();
formEvent();
solutionEvent();