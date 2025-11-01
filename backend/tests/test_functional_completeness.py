import requests

features = {
    "Health check": "http://127.0.0.1:8000/api/health",
    "Resume Parser": "http://127.0.0.1:8000/api/parse_resume",
    "JD Matcher": "http://127.0.0.1:8000/api/match_jd",
    "Question Generator": "http://127.0.0.1:8000/api/generate_questions",
}

missing = []
for feature, url in features.items():
    try:
        r = requests.get(url)
        if r.status_code != 200:
            missing.append(feature)
    except:
        missing.append(feature)

if missing:
    print("❌ Missing features:", missing)
else:
    print("✅ All core features implemented")