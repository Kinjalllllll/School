from fastapi import APIRouter,Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List
import model,schema,oauth2
import database
from sqlalchemy.orm import joinedload
from typing import Optional
import database
import redis
from fastapi_pagination import Page, add_pagination, paginate
from .enums import SortByEnum

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)



router = APIRouter()
model.Base.metadata.create_all(bind=database.engine)

@router.get("/students/", response_model=Page[schema.Student], tags=["student"])
def get_all_students(
    db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user),
    

    name: Optional[str] = Query(),
    min_age: Optional[int] = Query(),
    max_age: Optional[int] = Query(),
    sort_by: SortByEnum = Query(SortByEnum.id),
    order: str = Query("asc"),):

    if name:
        query = query.filter(model.Student.name.ilike(f"%{name}%"))
    if min_age is not None:
        query = query.filter(model.Student.age >= min_age)
    if max_age is not None:
        query = query.filter(model.Student.age <= max_age)
   
        query = db.query(model.Student)

    sort_column = getattr(model.Student, sort_by.value)
    if order.lower() == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()
    query = query.order_by(sort_column)
    students = query.all()

    return paginate(students)


@router.post("/students/", response_model=schema.Student, status_code=201,tags=['student'])
def create_student(request: schema.StudentCreate, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):

    new_student = model.Student(name=request.name, age=request.age)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    r.hset(f"student:{new_student.id}", mapping={
        "name": new_student.name,
        "age": new_student.age
    })
    return new_student


   
@router.get("/students/{student_id}", response_model=schema.Student,tags=['student'])
def read_student(student_id: int, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
  
    cached_student = r.hgetall(f"student:{student_id}")
    if cached_student:
        name = cached_student.get(b"name", b"")()
        age = int(cached_student.get(b"age", b""))
        return {"id": student_id, "name": name, "age": age}
    student = db.query(model.Student).filter(model.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    r.hset(f"student:{student.id}", mapping={
        "name": student.name,
        "age": student.age
    })
    return student


@router.delete('/students/{student_id}',tags=['student'])
def destroy(student_id: int, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    db.query(model.Student).filter(model.Student.id == student_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Student deleted successfully"}


@router.put("/student/{student_id}",tags=['student'])
def update_student(student_id: int, student_update: schema.StudentUpdate, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    student = db.query(model.Student).filter(model.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    
    student.name = student_update.name
    student.age = student_update.age

    db.commit()
    db.refresh(student) 

    return {"message": "Student has been updated", "student": {"id": student.id, "name": student.name, "age": student.age}}

@router.get("/teachers/", response_model=List[schema.Teacher],tags=['teacher'])
def read_teachers(db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    teachers = db.query(model.Teacher).all()
    return teachers

@router.post("/teachers/", response_model=schema.Teacher,status_code=201,tags=['teacher'])
def create_teacher(request: schema.TeacherCreate,db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    new_teacher = model.Teacher(teacher_name=request.teacher_name)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher



@router.delete('/teachers/{teacher_id}',tags=['teacher'])
def destroy(teacher_id: int, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    db.query(model.Teacher).filter(model.Teacher.id == teacher_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.put("/teachers/{teacher_id}",tags=['teacher'])

def update_teachers(teacher_id: int, teacher_update: schema.TeacherUpdate, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    teacher = db.query(model.Teacher).filter(model.Teacher.id == teacher_id).first()
    if not teacher_id:
        raise HTTPException(status_code=404, detail="Teacher not found")

    teacher.name = teacher_update.name

    db.commit()
    db.refresh(teacher) 

    return {"message": "Student has been updated", "student": {"id": teacher.id, "name": teacher.name}}



@router.get("/courses/{course_id}", response_model=schema.Course,tags=['course'])
def read_course(course_id: int, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    course = db.query(model.Course).filter(model.Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/courses/", response_model=schema.Course, status_code=201,tags=['course'])
def create_course(request: schema.CourseCreate, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    print("request", request)
    if request.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be greater than 0")

    existing_course = db.query(model.Course).filter(model.Course.course_name == request.course_name).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this name already exists")

    new_course = model.Course(
        course_name=request.course_name,
        teacher_id =request.teacher_id,
        student_id =request.student_id,
        credits=request.credits
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.put("/course/{course_id}",tags=['course'])
def update_course(course_id: int, course_update: schema.CourseUpdate, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):

    course = db.query(model.Course).filter(model.Course.id == course_id).first()
    if not course_id:
        print("no course found")
    else:
        raise HTTPException(status_code=404, detail="Course not found")

    course.name = course_update.course_name
    db.commit()
    db.refresh(course) 

    return {"message": "Course has been updated", "course": {"id": course.id, "name": course.course_name}}

@router.get("/courses/{course_id}/enroll/{student_id}/teacher{teacher_id}", response_model=schema.Course, tags=['course'])
def enroll_student(course_id: int, student_id: int, teacher_id:int, db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
   course = db.query(model.Course).options(joinedload(model.Course.students)).filter(model.Course.id == course_id).first()
   student = db.query(model.Student).filter(model.Student.id == student_id).first()

   if not course or not student:
        raise HTTPException(status_code=404, detail="Course or Student not found")


   db.commit()
   db.refresh(course)
   return course


