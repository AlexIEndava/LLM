# backend/app.py

import os
from flask import Flask, send_from_directory, jsonify, request
from backend.routes.recommend import recommend_router
from backend.routes.summary import summary_router

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../fronted"),
    static_url_path="/static"
)

# Servește index.html la rădăcina aplicației
@app.route("/")
def serve_ui():
    return send_from_directory(app.static_folder, "index.html")

# Servește fișiere statice (css, js, etc.)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Înregistrează rutele API
app.register_blueprint(recommend_router, url_prefix="/recommend")
app.register_blueprint(summary_router, url_prefix="/summary")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
