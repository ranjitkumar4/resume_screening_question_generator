import json
from app.services.resume_parser import parse_resume

with open("test_data/ground_truth.json") as f:
    ground_truth = json.load(f)

correct, total = 0, 0

for resume, expected in ground_truth.items():
    parsed = parse_resume(f"test_data/resumes/{resume}")
    for field, exp_val in expected.items():
        if field in parsed and parsed[field] == exp_val:
            correct += 1
        total += 1

accuracy = correct / total * 100
print(f"Resume Parse Accuracy: {accuracy:.2f}%")
assert accuracy >= 90