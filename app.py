import os

from flask import Flask, render_template, request, redirect, session
from database import create_tables, save_assessment, seed_questions, get_db_connection, save_response

app = Flask(__name__)
create_tables()
seed_questions()

app.secret_key = os.environ.get(
    "SECRET_KEY",
"wireless-security-assessment"
)

@app.route("/")
def home():
    return redirect("/demographic")


@app.route("/demographic", methods=["GET", "POST"])
def demographic():

    if request.method == "POST":

        session["status"] = request.form.get("status")
        session["level"] = request.form.get("level")
        session["faculty"] = request.form.get("faculty")
        session["wifi_frequency"] = request.form.get("wifi_frequency")
        session["device"] = request.form.get("device")
        session["experience"] = request.form.get("experience")

        return redirect("/knowledge")

    return render_template("demographic.html")




@app.route("/knowledge", methods=["GET", "POST"])
def knowledge():

    if request.method == "POST":

        score = 0

        questions = [
            "q7", "q8", "q9", "q10",
            "q11", "q12", "q13", "q14"
        ]

        for question in questions:

            answer = request.form.get(question)

            if answer:
                score += int(answer)

        session["knowledge_score"] = score

        return redirect("/authentication")

    return render_template("knowledge.html")



@app.route("/authentication", methods=["GET", "POST"])
def authentication():

    if request.method == "POST":

        score = 0

        questions = [
            ("q15", 15),
            ("q16", 16),
            ("q17", 17),
            ("q18", 18),
            ("q19", 19),
            ("q20", 20),
            ("q21", 21),
            ("q22", 22),
            ("q23", 23),
            ("q24", 24)
        ]

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                score += int(answer)

        authentication_score = (score / 50) * 40

        session["authentication_score"] = round(
            authentication_score, 2
        )

        # Temporarily store the individual answers
        session["authentication_responses"] = [
            {
                "question_id": question_id,
                "response": request.form.get(question_name),
                "score": int(request.form.get(question_name))
            }
            for question_name, question_id in questions
        ]

        return redirect("/protection")

    return render_template("authentication.html")



@app.route("/protection", methods=["GET", "POST"])
def protection():

    if request.method == "POST":

        score = 0

        questions = [
            ("q25", 25),
            ("q26", 26),
            ("q27", 27),
            ("q28", 28),
            ("q29", 29),
            ("q30", 30),
            ("q31", 31),
            ("q32", 32),
            ("q33", 33),
            ("q34", 34)
        ]

        protection_responses = []

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                answer_score = int(answer)
                score += answer_score

                protection_responses.append({
                    "question_id": question_id,
                    "response": answer,
                    "score": answer_score
                })

        protection_score = (score / 50) * 40

        session["protection_score"] = round(protection_score, 2)
        session["protection_responses"] = protection_responses

        return redirect("/access_control")

    return render_template("protection.html")



@app.route("/access_control", methods=["GET", "POST"])
def access_control():

    if request.method == "POST":

        score = 0

        questions = [
            ("q35", 35),
            ("q36", 36),
            ("q37", 37),
            ("q38", 38),
            ("q39", 39),
            ("q40", 40),
            ("q41", 41),
            ("q42", 42),
            ("q43", 43),
            ("q44", 44)
        ]

        access_control_responses = []

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                answer_score = int(answer)
                score += answer_score

                access_control_responses.append({
                    "question_id": question_id,
                    "response": answer,
                    "score": answer_score
                })

        access_control_score = (score / 50) * 40

        session["access_control_score"] = round(access_control_score, 2)
        session["access_control_responses"] = access_control_responses

        return redirect("/configuration")

    return render_template("access_control.html")


@app.route("/configuration", methods=["GET", "POST"])
def configuration():

    if request.method == "POST":

        score = 0

        questions = [
            ("q45", 45),
            ("q46", 46),
            ("q47", 47),
            ("q48", 48),
            ("q49", 49),
            ("q50", 50),
            ("q51", 51),
            ("q52", 52),
            ("q53", 53),
            ("q54", 54)
        ]

        configuration_responses = []

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                answer_score = int(answer)
                score += answer_score

                configuration_responses.append({
                    "question_id": question_id,
                    "response": answer,
                    "score": answer_score
                })

        configuration_score = (score / 50) * 40

        session["configuration_score"] = round(configuration_score, 2)
        session["configuration_responses"] = configuration_responses

        return redirect("/monitoring")

    return render_template("configuration.html")


@app.route("/monitoring", methods=["GET", "POST"])
def monitoring():

    if request.method == "POST":

        score = 0

        questions = [
            ("q55", 55),
            ("q56", 56),
            ("q57", 57),
            ("q58", 58),
            ("q59", 59),
            ("q60", 60),
            ("q61", 61),
            ("q62", 62),
            ("q63", 63),
            ("q64", 64)
        ]

        monitoring_responses = []

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                answer_score = int(answer)
                score += answer_score

                monitoring_responses.append({
                    "question_id": question_id,
                    "response": answer,
                    "score": answer_score
                })

        monitoring_score = (score / 50) * 40

        session["monitoring_score"] = round(monitoring_score, 2)
        session["monitoring_responses"] = monitoring_responses

        return redirect("/awareness")

    return render_template("monitoring.html")


@app.route("/awareness", methods=["GET", "POST"])
def awareness():

    if request.method == "POST":

        score = 0

        questions = [
            ("q65", 65),
            ("q66", 66),
            ("q67", 67),
            ("q68", 68),
            ("q69", 69),
            ("q70", 70),
            ("q71", 71),
            ("q72", 72),
            ("q73", 73),
            ("q74", 74)
        ]

        awareness_responses = []

        for question_name, question_id in questions:

            answer = request.form.get(question_name)

            if answer:
                answer_score = int(answer)
                score += answer_score

                awareness_responses.append({
                    "question_id": question_id,
                    "response": answer,
                    "score": answer_score
                })

        awareness_score = (score / 50) * 40

        session["awareness_score"] = round(awareness_score, 2)
        session["awareness_responses"] = awareness_responses

        return redirect("/result")

    return render_template("awareness.html")


@app.route("/result")
def result():

    authentication = session.get("authentication_score", 0)
    protection = session.get("protection_score", 0)
    access_control = session.get("access_control_score", 0)
    configuration = session.get("configuration_score", 0)
    monitoring = session.get("monitoring_score", 0)
    awareness = session.get("awareness_score", 0)

    total_score = (
        authentication
        + protection
        + access_control
        + configuration
        + monitoring
        + awareness
    )

    maximum_score = 240

    percentage = (total_score / maximum_score) * 100

    if percentage >= 80:
        level = "Strong"

    elif percentage >= 60:
        level = "Moderate"

    elif percentage >= 40:
        level = "Weak"

    else:
        level = "Critical"

    # Save the overall assessment
    assessment_id = save_assessment(
        total_score,
        percentage,
        level
    )

    # Save responses from all six sections
    response_sections = [
        "authentication_responses",
        "protection_responses",
        "access_control_responses",
        "configuration_responses",
        "monitoring_responses",
        "awareness_responses"
    ]

    for section in response_sections:

        responses = session.get(section, [])

        for response in responses:

            save_response(
                assessment_id,
                response["question_id"],
                response["response"],
                response["score"]
            )

    return render_template(
        "result.html",
        authentication=authentication,
        protection=protection,
        access_control=access_control,
        configuration=configuration,
        monitoring=monitoring,
        awareness=awareness,
        total_score=round(total_score, 2),
        maximum_score=maximum_score,
        percentage=round(percentage, 2),
        level=level
    )


if __name__ == "__main__":
    app.run(debug=True)