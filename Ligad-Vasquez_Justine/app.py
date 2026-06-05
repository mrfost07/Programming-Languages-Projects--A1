from flask import Flask, render_template, request
import io
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""

    if request.method == "POST":
        code = request.form["code"]

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            exec(code)
            output = buffer.getvalue()
        except Exception as e:
            output = f"Error: {e}"

        sys.stdout = old_stdout

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)