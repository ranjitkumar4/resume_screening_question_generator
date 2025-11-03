def lookup_skill(skill_name):
    try:
        skill_trends = {
            "Python": "High demand, trending upward",
            "SQL": "Steady demand",
            "FastAPI": "Growing rapidly",
            "Java": "Mature, steady demand",
            "React": "High demand, trending upward",
        }
        return skill_trends.get(skill_name, "Unknown skill trend")
    except Exception as e:
        print("Tool lookup failed:", e)
        return "Error"