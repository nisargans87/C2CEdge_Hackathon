import os
import uuid
import asyncio

from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from dotenv import load_dotenv

from realitychecker import check_news_image


# ============================================================
# LOAD ENV
# ============================================================

load_dotenv()


# ============================================================
# FLASK
# ============================================================

app = Flask(
    __name__,
    template_folder="web",
    static_folder="web",
    static_url_path="/static"
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_FOLDER = Path(
    "web_uploads"
)

UPLOAD_FOLDER.mkdir(
    exist_ok=True
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# ANALYZE
# ============================================================

@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze():

    file = request.files.get(
        "file"
    )

    if not file:

        return jsonify({
            "success": False,
            "error": "No file uploaded."
        }), 400


    if not file.filename:

        return jsonify({
            "success": False,
            "error": "Invalid file."
        }), 400


    # --------------------------------------------------------
    # EXTENSION
    # --------------------------------------------------------

    extension = Path(
        file.filename
    ).suffix.lower()


    allowed_extensions = {

        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
        ".mp4",
        ".mov",
        ".webm"

    }


    if extension not in allowed_extensions:

        return jsonify({
            "success": False,
            "error": "Unsupported file type."
        }), 400


    # --------------------------------------------------------
    # UNIQUE FILE
    # --------------------------------------------------------

    filename = (
        str(uuid.uuid4())
        + extension
    )

    file_path = (
        UPLOAD_FOLDER /
        filename
    )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    file.save(
        str(file_path)
    )


    print(
        "File received:",
        file_path
    )


    try:

        # ----------------------------------------------------
        # CURRENT VERSION
        #
        # We are focusing on IMAGE first.
        # ----------------------------------------------------

        if extension in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif"
        ]:

            result = check_news_image(
                str(file_path)
            )

        else:

            return jsonify({
                "success": False,
                "error":
                    "Video UI is ready, "
                    "but video verification will "
                    "be connected next."
            }), 400


        return jsonify({

            "success": True,

            "result": result

        })


    except Exception as error:

        print(
            "Analysis error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


    finally:

        # ----------------------------------------------------
        # DELETE FILE
        # ----------------------------------------------------

        try:

            if file_path.exists():

                file_path.unlink()

        except Exception:

            pass


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )

    print(
        "       TRUST CHECKER WEB APP"
    )

    print(
        "======================================"
    )

    print(
        "Open: http://127.0.0.1:5000"
    )

    print(
        "======================================"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )