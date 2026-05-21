from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]

        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(UPLOAD_FOLDER, "cleaned.xlsx")

            file.save(input_path)

            df = pd.read_excel(input_path)

            # Clean Data
            df.drop_duplicates(inplace=True)
            df.fillna("", inplace=True)

            df.to_excel(output_path, index=False)

            return send_file(output_path, as_attachment=True)

    return render_template("index.html")

app.run(host="0.0.0.0", port=81)
