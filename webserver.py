from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def meows():
    count:int = read_count()
    print(count)
    return render_template("index.html", meow_count=count)

def send_update():
    print("Forcing refresh...")

def read_count():
    try:
        file = open('count.txt', 'r')
        count = int(file.read())
        return count
    except (FileNotFoundError, ValueError):
        return 0  # Default value if file doesn't exist

def run_flask():
    app.run()


