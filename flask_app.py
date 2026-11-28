 
from flask import Flask, render_template, request, jsonify, Response

from src.web_backend import (
    restore_with_opencv,
    restore_with_realesrgan
)

app = Flask(__name__)


# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# IMAGE RESTORATION API
# =====================================

@app.route("/api/restore", methods=["POST"])
def restore_image():

    try:
        # Receive uploaded image
        if "image" not in request.files:
            return jsonify({
                "error": "No image was uploaded."
            }), 400

        uploaded_file = request.files["image"]

        if uploaded_file.filename == "":
            return jsonify({
                "error": "Please select an image."
            }), 400

        uploaded_image = uploaded_file.read()

        if not uploaded_image:
            return jsonify({
                "error": "The uploaded file is empty."
            }), 400

        # Receive restoration settings
        method = request.form.get("method")
        category = request.form.get("category")

        # Select restoration method
        if method == "opencv":

            restored_image, processing_time = (
                restore_with_opencv(uploaded_image, category)
            )

        elif method == "realesrgan":

            restored_image, processing_time = (
                restore_with_realesrgan(uploaded_image)
            )

        else:
            return jsonify({
                "error": "Invalid restoration method."
            }), 400

        # Return restored image to browser
        return Response(
            restored_image,
            mimetype="image/png",
            headers={
                "X-Processing-Time": str(processing_time)
            }
        )

    except Exception as error:

        print("RESTORATION ERROR:", error)

        return jsonify({
            "error": str(error)
        }), 500


# =====================================
# RUN FLASK APPLICATION
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
