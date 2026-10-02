import os
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory

from project_builder import ProjectBuilder

EDITOR_FILES = ("index.html", "style.css", "script.js")


def _project_directory(project_name: str) -> Path | None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_name):
        return None
    return Path(__file__).resolve().parent / "generated_projects" / project_name


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "provider": os.getenv("LLM_PROVIDER", "ollama")})

    @app.get("/projects/<project_name>/")
    def project_preview(project_name: str):
        project_root = _project_directory(project_name)
        if project_root is None or not project_root.is_dir():
            return jsonify({"error": "Project not found."}), 404
        return send_from_directory(str(project_root), "index.html")

    @app.get("/projects/<project_name>/<path:filename>")
    def project_asset(project_name: str, filename: str):
        project_root = _project_directory(project_name)
        if project_root is None or not project_root.is_dir():
            return jsonify({"error": "Project not found."}), 404
        return send_from_directory(str(project_root), filename)

    @app.get("/api/projects/<project_name>/files")
    def read_project_files(project_name: str):
        project_root = _project_directory(project_name)
        if project_root is None or not project_root.is_dir():
            return jsonify({"error": "Project not found."}), 404
        files = {
            filename: (project_root / filename).read_text(encoding="utf-8")
            for filename in EDITOR_FILES
            if (project_root / filename).is_file()
        }
        return jsonify({"files": files})

    @app.post("/api/projects/<project_name>/files/<filename>")
    def save_project_file(project_name: str, filename: str):
        project_root = _project_directory(project_name)
        if project_root is None or not project_root.is_dir():
            return jsonify({"error": "Project not found."}), 404
        if filename not in EDITOR_FILES:
            return jsonify({"error": "This file cannot be edited here."}), 400

        data = request.get_json(silent=True) or {}
        content = data.get("content")
        if not isinstance(content, str):
            return jsonify({"error": "File content must be text."}), 400
        if len(content) > 1_000_000:
            return jsonify({"error": "Files must be smaller than 1 MB."}), 413

        (project_root / filename).write_text(content, encoding="utf-8")
        return jsonify({"saved": True, "filename": filename})

    @app.post("/api/generate")
    def generate_project():
        data = request.get_json(silent=True) or {}
        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        builder = ProjectBuilder(output_dir="generated_projects")
        project_path = builder.build_from_prompt(prompt)
        preview_url = f"http://127.0.0.1:5000/projects/{project_path.name}/"
        return jsonify({
            "project_name": project_path.name,
            "project_path": str(project_path),
            "preview_url": preview_url,
            "message": "Your website is ready to preview.",
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
