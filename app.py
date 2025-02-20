import logging
import random
import os
from flask import Flask, jsonify, render_template, session

app = Flask(__name__, template_folder=os.path.abspath("templates"))  # templates 폴더 위치 명확히 지정
app.secret_key = 'your_secret_key'  # 세션을 사용하기 위한 키 설정

# 로그 설정 추가
logging.basicConfig(level=logging.DEBUG)

# A, B 그룹 설정
groups = {
    "A": ["브라질", "독일", "프랑스"],
    "B": ["스페인", "아르헨티나", "잉글랜드", "이탈리아", "포르투갈", "네덜란드", "벨기에"]
}

def select_team(mode):
    selected_teams = session.get("selected_teams", [])  # 이미 선택된 팀 목록 가져오기
    
    # 선택 가능한 팀 필터링
    available_teams = {
        "A": [team for team in groups["A"] if team not in selected_teams],
        "B": [team for team in groups["B"] if team not in selected_teams]
    }
    
    # 모든 팀이 선택된 경우
    if not available_teams["A"] and not available_teams["B"]:
        return "모든 팀이 선택되었습니다."
    
    # 그룹 선택 확률 설정
    if mode == "normal":
        group_weights = [0.35, 0.65]  # 일반 뽑기 A/B 그룹 확률 35%/65%
    else:
        group_weights = [0.75, 0.25]  # 진 팀 뽑기 A/B 그룹 확률 75%/25%
    
    # 선택할 그룹 결정 (A 또는 B 그룹이 소진되었을 경우 다른 그룹을 자동 선택)
    available_group_keys = [key for key in groups.keys() if available_teams[key]]
    
    if len(available_group_keys) == 1:
        chosen_group = available_group_keys[0]  # 하나의 그룹만 남았으면 무조건 선택
    else:
        chosen_group = random.choices(available_group_keys, weights=[group_weights[0] if key == "A" else group_weights[1] for key in available_group_keys], k=1)[0]
    
    # 해당 그룹 내에서 균등 확률로 팀 선택
    chosen_team = random.choice(available_teams[chosen_group])
    selected_teams.append(chosen_team)  # 선택된 팀 저장
    session["selected_teams"] = selected_teams  # 세션에 저장
    
    return chosen_team

@app.route('/')
def home():
    app.logger.info("홈 페이지 접근")
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"오류 발생: {e}")
        return "Internal Server Error", 500

@app.route('/gacha/normal', methods=['GET'])
def gacha_normal():
    result = select_team("normal")
    return jsonify({"result": result})

@app.route('/gacha/loser', methods=['GET'])
def gacha_loser():
    result = select_team("loser")
    return jsonify({"result": result})

@app.route('/reset', methods=['GET'])
def reset():
    session.pop("selected_teams", None)  # 선택된 팀 목록 초기화
    return jsonify({"message": "토너먼트 초기화 완료"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
