
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="수강기록 관리 API 서버")

JSON_FILE = "courses.json"

# 1. 수강기록 데이터 모델 정의 (Pydantic이 잘못된 데이터 타입을 자동 검증)
class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

# 2. JSON 파일 초기화 및 로드 함수
def load_courses() -> list:
    # 파일이 없으면 빈 리스트로 초기 생성
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # JSON 파일이 깨져있을 경우 예외 처리
        return []

# 3. JSON 파일 저장 함수
def save_courses(data: list):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# [GET] /courses - 전체 수강기록 조회
@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses


# [POST] /courses - 새로운 수강기록 추가
@app.post("/courses")
def add_course(course: Course):
    # JSON 파일에서 기존 데이터 로드
    courses = load_courses()
    
    # Pydantic 모델을 dict로 변환 후 append
    new_course = course.model_dump()
    courses.append(new_course)
    
    # 파일에 다시 저장
    save_courses(courses)
    
    return {"message": "수강기록이 성공적으로 추가되었습니다.", "data": new_course}
