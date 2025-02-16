from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # ✅ .env 파일 로드

login_url = os.getenv("NAVER_LOGIN_URL", "https://nid.naver.com/nidlogin.login")

# ✅ 로그인 필드 선택자 불러오기
id_selector = os.getenv("NAVER_ID_SELECTOR", "#id")
pw_selector = os.getenv("NAVER_PASSWORD_SELECTOR", "#pw")

# ✅ JSON 형태의 계정 리스트 불러오기

# ✅ Chrome 프로필 경로 (기존 브라우저 유지)
chrome_profile = os.getenv("CHROME_USER_DATA_DIR", None)

def run_automation(name, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        # ✅ 로그인 페이지 URL도 환경 변수에서 불러오기 가능
        login_url = os.getenv("NAVER_LOGIN_URL", "https://nid.naver.com/nidlogin.login")
        page.goto(login_url)

        # ✅ .env에서 필드명을 동적으로 가져오기
        id_selector = os.getenv("NAVER_ID_SELECTOR", "#id")
        pw_selector = os.getenv("NAVER_PASSWORD_SELECTOR", "#pw")

        # ✅ 동적으로 입력 필드 값 설정
        page.fill(id_selector, name)
        page.fill(pw_selector, password)

        page.wait_for_timeout(3000)  # 3초 대기 (UI 반영)

        print(f"🚀 로그인 완료: {name}")
        input("❗ 브라우저를 닫은 후 엔터를 눌러 프로그램을 종료하세요...")

        browser.close()

@app.route("/puppeteer/run", methods=["POST"])
def run():
    data = request.json  
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format, expected a list"}), 400
    
    for item in data:
        run_automation(item["name"], item["password"])

    return jsonify({"message": "Automation executed successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)