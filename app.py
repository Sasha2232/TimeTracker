from flask import Flask, render_template, request, redirect, jsonify
import datetime
from database import Database
from bot_logic import Bot

app = Flask(__name__)
db = Database()
bot = Bot()


@app.route("/")
def index():
    tasks = db.get_all_tasks()
    total = sum(t["seconds"] for t in tasks)

    today = datetime.date.today()
    week_data = {str(today - datetime.timedelta(days=i)): 0 for i in range(6, -1, -1)}
    for t in tasks:
        if t["date"] in week_data:
            week_data[t["date"]] += t["seconds"]

    return render_template("index.html",
                           tasks=tasks,
                           total=total,
                           labels=list(week_data.keys()),
                           values=list(week_data.values()))


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("task", "").strip()
    if name:
        db.add_task(name)
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
    db.delete_task(task_id)
    return redirect("/")


@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    try:
        seconds = int(request.form.get("seconds", 0))
    except ValueError:
        seconds = 0
    db.update_task_seconds(task_id, seconds)
    return redirect("/")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Пустое сообщение."})
    db.save_message("user", user_message)
    reply = bot.handle(user_message)
    db.save_message("bot", reply)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
