from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def checklist_page() -> str:
    return render_template("checklist_page.html")
    