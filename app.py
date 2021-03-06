""" Survey Exercise"""

from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# responses = []
SURVEY = ""


@app.route("/", methods=["GET"])
def begin():
    return render_template("begin.html")


@app.route("/session", methods=["POST"])
def start():
    session["responses"] = []
    return render_template("start.html", surveys=surveys)


@app.route("/home", methods=["POST"])
def home():
    global SURVEY

    if "choice" not in request.form.keys():
        flash("Must select survey or test")
        return redirect("/")

    SURVEY = surveys[request.form["choice"]]
    return render_template("home.html", survey=SURVEY)


@app.route("/questions/<int:question_num>")
def questions(question_num):
    """ask specified question # """
    # if all questions asked any attempt to get question by id returns to Thank You page

    responses = session["responses"]
    if len(responses) == len(SURVEY.questions):
        return render_template("/thankyou.html", survey=SURVEY, responses=responses)

    # if requested question #(a 0 based index) is not equal
    # to the number of questions answered, set the question #
    # to be asked (an index) to the number of reponses. because of
    # 0 based index, number of responses = index of next question

    if question_num != len(responses):
        flash("Attempt to access questions out of order denied")
        question_num = len(responses)

    return render_template("questions.html", question=SURVEY.questions[question_num])


@app.route("/answer", methods=["POST", "GET"])
def answer():
    """store response to question. ask next question"""
    responses = session["responses"]

    if "choice" in request.form.keys():
        responses.append(request.form["choice"])
        session["responses"] = responses

    # if # of responses = # of questions then completed
    if len(responses) == len(SURVEY.questions):
        return render_template("/thankyou.html", survey=SURVEY, responses=responses)

    # {len(responses)} = ask next question based on # of answers
    return redirect(f"/questions/{len(responses)}")
