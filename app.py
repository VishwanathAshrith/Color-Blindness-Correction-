from flask import Flask, request, jsonify, send_from_directory, render_template
import os, sys, uuid, subprocess
from recolor import Core
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


# =====================
# PAGE ROUTES
# =====================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("next.html")

@app.route("/image")
def image():
    return render_template("image.html")

@app.route("/camera")
def camera():
    return render_template("camera.html")

@app.route("/video")
def video():
    return render_template("video.html")


# =====================
# CORE PROCESSING
# =====================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/generate", methods=["POST"])
@app.route("/generate", methods=["POST"])
def generate():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    blindness_type = request.form.get("type")

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Clear old outputs
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))

    file_ext = os.path.splitext(filename)[-1]
    output_filename = f"corrected_{blindness_type}{file_ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        if blindness_type == "protanopia":
            Core.correct(
                input_path=input_path,
                return_type="save",
                save_path=output_path,
                protanopia_degree=0.9,
                deutranopia_degree=0.0
            )

        elif blindness_type == "deutranopia":
            Core.correct(
                input_path=input_path,
                return_type="save",
                save_path=output_path,
                protanopia_degree=0.0,
                deutranopia_degree=1.0
            )

        elif blindness_type == "tritanopia":
            Core.correct(
                input_path=input_path,
                return_type="save",
                save_path=output_path,
                protanopia_degree=0.0,
                deutranopia_degree=0.0
            )

        elif blindness_type == "hybrid":
            Core.correct(
                input_path=input_path,
                return_type="save",
                save_path=output_path,
                protanopia_degree=0.5,
                deutranopia_degree=0.5
            )

        else:
            return jsonify({"error": "Invalid blindness type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"output_images": [output_filename]})


# =====================
# OUTPUT FILES
# =====================

@app.route("/output/<path:filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)