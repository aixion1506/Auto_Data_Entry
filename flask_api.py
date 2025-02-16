from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def run_automation(name, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)  # 브라우저 실행
        page = browser.new_page()
        
        # 네이버 로그인 페이지로 이동
        page.goto("https://nid.naver.com/nidlogin.login")

        # 아이디와 비밀번호 입력
        page.fill("#id", name)
        page.fill("#pw", password)

        page.wait_for_timeout(3000)  # 3초 대기 (UI 반영)

        browser.close()  # 브라우저 종료

@app.route("/puppeteer/run", methods=["POST"])
def run():
    data = request.json  # JSON 데이터 받기
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format, expected a list"}), 400
    
    for item in data:
        run_automation(item["name"], item["password"])

    return jsonify({"message": "Automation executed successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)