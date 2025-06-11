from sqlalchemy import Column, Integer, String, ForeignKey, Table,Enum
from sqlalchemy.orm import relationship
from database import Base


course_student = Table(
    "course_student",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("student_id", ForeignKey("students.id"), primary_key=True),
)
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    courses = relationship("Course", back_populates="students")


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String)

    courses = relationship("Course", back_populates="teachers")


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    student_id = Column(Integer,ForeignKey('students.id'))
    credits = Column(Integer, nullable=True)

    teachers = relationship("Teacher", back_populates="courses")
    students = relationship("Student", back_populates="courses")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)




