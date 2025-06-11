from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional


class StudentBase(BaseModel):
    name: str
    age: int

class StudentCreate(StudentBase):
    name: str
    age: int

class StudentUpdate(StudentBase):
    model_config = ConfigDict(from_attributes=True)

class Student(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



class TeacherBase(BaseModel):
    teacher_name: str


class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    teacher_name:str
    model_config = ConfigDict(from_attributes=True)

class TeacherUpdate(BaseModel):
    teacher_name: str


class CourseBase(BaseModel):
    teacher_id : int
    course_name : str
    student_id : int
    credits: Optional[int] = None

class CourseCreate(BaseModel):
    teacher_id : int
    student_id : int
    course_name : str
    credits: Optional[int] = None

class Course(CourseBase):
    id: int
    teacher_id: int
    student_id: int
 

class CourseUpdate(BaseModel):
    course_name: str   
    model_config = ConfigDict(from_attributes=True)

class StatusResponse(BaseModel):
    message: str


class User(BaseModel):
    name : str
    email : str
    password : str

class ShowUser(BaseModel):
    id : int
    username : str
    email : str


model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username : str
    email :str

class Login(BaseModel):
    username : str
    password : str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

class Email(BaseModel):
    email: list[EmailStr]
    body: dict[str, str] |None = None  
    
class EmailSchema(BaseModel):
    email: List[EmailStr]  

class Token(BaseModel):
    create_access_token: str
    token_type : str


class TokenData(BaseModel):
    username : str

model_config = ConfigDict(from_attributes=True)

