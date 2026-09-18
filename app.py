from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Good Job Services is Live!"

if __name__ == "__main__":
    app.run()
