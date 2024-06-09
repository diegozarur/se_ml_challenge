from flask import Blueprint, request, jsonify, current_app, send_file, url_for
from app.tasks import ask_question
import os
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)

ALLOWED_EXTENSIONS = {".pdf"}


@api_bp.route("/documents", methods=["POST"])
def upload_document():
    if "files" not in request.files:
        return jsonify({"error": "No files part in the request"}), 400
    try:
        files = request.files.getlist("files")
        docs_dir = current_app.config["UPLOAD_FOLDER"]

        for file in files:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                return jsonify({"message": f"Unsupported file type - file=>{file}"}), 400
            file.save(os.path.join(docs_dir, file.filename))

        return jsonify({"message": "Document uploaded successfully"}), 202
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@api_bp.route("/ask", methods=["POST"])
def ask_question_route():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"message": "Question is required"}), 400

        # Call the Celery task to ask a question
        result = ask_question.apply_async((question,))

        return jsonify({"task_id": result.id}), 202
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@api_bp.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    task = ask_question.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"status": "Pending"}), 202
    elif task.state != "FAILURE":
        response = task.result
        response["file"] = url_for(
            "api.download_file", filename=response.get("file", ""), _external=True
        )
        return jsonify(response), 200
    else:
        return jsonify({"message": str(task.info)}), 500


@api_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_file(
        os.path.join(current_app.config["UPLOAD_FOLDER"], filename),
        mimetype="application/pdf",
    )
