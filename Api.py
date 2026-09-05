from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from main import calculate_result


app = FastAPI(
    title="Student Report Generator API",
    description="Backend API for automated student report generation",
    version="1.0.0",
)


class Student(BaseModel):
    name: str
    python: float
    dbms: float
    java: float


@app.get("/")
def root():
    return {
        "message": "Student Report Generator API is running"
    }


@app.post("/report")
def create_report(student: Student):
    try:
        result = calculate_result(student.model_dump())
        return result
    except (KeyError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
)
