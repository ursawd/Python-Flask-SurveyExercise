""" Survey Exercise"""

from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys
from random import choice

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []
#! why does one work and one doesnt.
# SURVEY_NAME = Survey
key = choice(list(surveys))
SURVEY_NAME = surveys[key]


@app.route("/")
def start():
    return render_template("start.html", surveys=surveys)


@app.route("/home", methods=["POST"])
def home():
    # TODO    receive survey selection and start
    #!----optional initialization code result in this and next red text------
    #!Here SURVEY_NAME has valid data and this route works
    #!      (Pdb) len(SURVEY_NAME.questions)
    #!      4
    #!      (Pdb)
    SURVEY_NAME = surveys[request.form["choice"]]
    # import pdb
    # pdb.set_trace()

    return render_template("home.html", survey=SURVEY_NAME)


@app.route("/questions/<int:question_num>")
def questions(question_num):
    """ask specified question # """

    # import pdb
    # pdb.set_trace()
    #! Here SURVEY_NAME has no questions, title,etc data and route errors out
    #!      (Pdb) len(SURVEY_NAME.questions)
    #!      *** AttributeError: type object 'Survey' has no attribute 'questions'
    #!      (Pdb)

    if len(responses) == len(SURVEY_NAME.questions):
        return render_template("/thanks.html", answers=responses)

    # if requested question #(a 0 based index) is not equal
    # to the number of questions answered, set the question #
    # to be asked (an index) to the number of reponses. because of
    # 0 based index, number of responses = index of next question

    if question_num != len(responses):
        flash("Attempt to access questions out of order denied")
        question_num = len(responses)

    return render_template("questions.html", question=SURVEY_NAME.questions[question_num])


@app.route("/answer", methods=["POST"])
def answer():
    """store response to question. ask next question"""
    responses.append(request.form["choice"])

    # if # of responses = # of questions then completed
    if len(responses) == len(SURVEY_NAME.questions):
        return render_template("/thanks.html")

    # {len(responses)} = ask next question based on # of answers
    return redirect(f"/questions/{len(responses)}")