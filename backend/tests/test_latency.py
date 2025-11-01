import requests, time

endpoints = [
    "http://127.0.0.1:8000/api/parse_resume",
    "http://127.0.0.1:8000/api/match_jd",
    "http://127.0.0.1:8000/api/generate_questions",
]

for url in endpoints:
    start = time.time()
    r = requests.get(url)
    latency = time.time() - start
    print(f"{url} latency: {latency:.2f}s")
    assert latency <= 3