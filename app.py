""" Survey Exercise"""

from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []
SURVEY_NAME = satisfaction_survey


@app.route("/")
def home():
    return render_template("home.html", survey=SURVEY_NAME)


@app.route("/questions/<int:question_num>")
def questions(question_num):
    return render_template("questions.html", question=SURVEY_NAME.questions[question_num])


@app.route("/answer", methods=["POST"])
def answer():
    responses.append(request.form["choice"])
    if len(responses) == len(SURVEY_NAME.questions):
        return render_template("/thanks.html")
    return redirect(f"/questions/{len(responses)}")