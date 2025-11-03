from backend.agents.resume_extractor_agent import extract_resume_info
from backend.agents.jd_matcher_agent import match_resume_to_jd
from backend.agents.qgen_agent import generate_questions
from backend.core.memory_manager import load_memory, save_memory

def run_supervisor(resume_text, jd_text, candidate_id="candidate_1"):
    memory = load_memory()
    try:
        # Step 1: Parse Resume
        parsed_resume = extract_resume_info(resume_text)
        memory[candidate_id] = {"parsed_resume": parsed_resume}

        # Step 2: JD Match
        match_result = match_resume_to_jd(resume_text, jd_text)
        memory[candidate_id]["jd_match"] = match_result

        # Step 3: Generate Questions
        # questions = generate_questions(parsed_resume, jd_text)
        # memory[candidate_id]["questions"] = questions

        # Save Memory
        save_memory(memory)
        return {
            "parsed_resume": parsed_resume,
            "jd_match": match_result,
            #"questions": questions
        }
    except Exception as e:
        print("Supervisor workflow failed:", e)
        return {}