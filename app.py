from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/gacha', methods=['GET'])
def gacha():
    items = ["전설 무기", "희귀 방어구", "일반 아이템", "포션"]
    probabilities = [0.05, 0.15, 0.5, 0.3]
    result = random.choices(items, weights=probabilities, k=1)[0]
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
