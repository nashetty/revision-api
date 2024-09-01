from flask import Flask, jsonify, request
from db_utils import (
    DbConnectionError,
    UserError,
    get_all_questions,
    get_question_by_id,
    get_questions_by_language,
    create_new_question,
    delete_question_by_id,
    update_mastery_by_id,
)


app = Flask(__name__)


# homepage
@app.route("/")
def index():
    return "Welcome to the REVISION"


# GET all questions
# no need to specify the method is GET as it is GET by default
@app.route("/questions")
def questions():
    try:
        res = get_all_questions()
        return jsonify(res)
    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


# GET question by id
@app.route("/questions/<id>")
def question_by_id(id):
    try:
        res = get_question_by_id(id)
        return jsonify(res)
    except UserError as e:
        return jsonify({"error": str(e)}), 404
    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


# GET question by Language
@app.route("/questions/language/<language>")
def questions_by_language(language):
    try:
        res = get_questions_by_language(language)
        return jsonify(res)
    except UserError as e:
        return jsonify({"error": str(e)}), 404
    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


# create/POST new question
@app.route("/questions", methods=["POST"])
def create_question():
    try:
        new_question = request.get_json()
        created_question = create_new_question(new_question)
        return jsonify(created_question), 201
    except UserError as e:
        return jsonify({"error": str(e)}), 400

    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


# DELETE question by id
@app.route("/questions/<id>", methods=["DELETE"])
def delete_question(id):
    try:
        delete_question_by_id(id)
        return jsonify({"message": "question deleted"})
    except UserError as e:
        return jsonify({"error": str(e)}), 404
    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


# update mastery with PATCH
@app.route("/questions/<id>", methods=["PATCH"])
def update_mastery(id):
    try:
        req = request.get_json()
        updated_record = update_mastery_by_id(id, req["mastery"])
        return jsonify(
            {
                "message": f"mastery for question {id} updated successfully to {req['mastery']}",
                "update": updated_record,
            }
        )
    except UserError as e:
        return jsonify({"error": str(e)}), 404
    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
