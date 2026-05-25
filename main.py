from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI(title="관리 서버")

JSON_FILE = "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_courses():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_courses(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        
@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses

@app.post("/courses")
def add_course(course: Course):
    courses = load_courses()
    new_course_dict = course.model_dump() 
    courses.append(new_course_dict)
    save_courses(courses)
    return {"message": "추가완료.", "data": new_course_dict}
