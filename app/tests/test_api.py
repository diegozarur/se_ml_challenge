import pytest
from pathlib import Path

resources = Path(__file__).parent / "docs"


@pytest.mark.task("api")
class TestRoutes:

    def test_upload_document(self, client):
        response = client.post(
            "/api/documents",
            data={
                "files": (resources / "sample.pdf").open("rb"),
            },
        )
        assert response.status_code == 202
        assert "Document uploaded successfully" in response.json["message"]

    def test_upload_document_invalid_file(self, client):
        response = client.post(
            "/api/documents",
            data={
                "files": (resources / "sample.txt").open("rb"),
            },
        )
        assert response.status_code == 400
        assert "Unsupported file type" in response.json["message"]

    def test_upload_document_no_file(self, client):
        response = client.post("/api/documents")
        assert response.status_code == 400
        assert "No files part in the request" in response.json["error"]

    def test_ask_question(self, client):
        response = client.post(
            "/api/ask", json={"question": "What is the main topic of the document?"}
        )
        assert response.status_code == 202
        assert "task_id" in response.json

    def test_ask_question_no_question(self, client):
        response = client.post("/api/ask", json={})
        assert response.status_code == 400
        assert "Question is required" in response.json["message"]

    def test_get_result(self, client):
        task_id = "sample_task_id"
        response = client.get(f"/api/result/{task_id}")
        assert response.status_code in [200, 202]  # If task is pending or completed

    def test_download_file(self, client):
        filename = "sample.pdf"
        response = client.get(f"/api/download/{filename}")
        assert response.status_code == 200
        assert response.mimetype == "application/pdf"
