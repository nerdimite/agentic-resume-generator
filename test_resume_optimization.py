import glob
import json
import os

from dotenv import load_dotenv

load_dotenv()

from resume_generator.models import Resume
from resume_generator.optimizer import ResumeOptimizer

RESUME_INPUT_DIR = "resume_input"
RESUME_OUTPUT_DIR = "resume_output"


def optimize_resume(
    job_description_path: str, resume_json_path: str, resume_output_path: str
):

    for file in glob.glob(f"{RESUME_INPUT_DIR}/*.pdf"):
        print(file)

    os.makedirs(RESUME_OUTPUT_DIR, exist_ok=True)

    with open(job_description_path, "r") as f:
        job_description = f.read()

    with open(resume_json_path, "r") as f:
        resume_json = json.load(f)
        resume = Resume.model_validate(resume_json)

    optimizer = ResumeOptimizer()
    optimized_resume = optimizer.optimize_resume(job_description, resume)

    with open(resume_output_path, "w") as f:
        f.write(optimized_resume.model_dump_json(indent=2))

    return optimized_resume


if __name__ == "__main__":
    job_description_path = f"{RESUME_INPUT_DIR}/job_description.txt"
    resume_json_path = f"{RESUME_INPUT_DIR}/Resume_of_Bhavesh_Laddagiri.json"

    resume_output_path = (
        f"{RESUME_OUTPUT_DIR}/Resume_of_Bhavesh_Laddagiri_optimized.json"
    )

    optimize_resume(job_description_path, resume_json_path, resume_output_path)
