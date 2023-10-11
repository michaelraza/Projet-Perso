from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from classes.schema_dto import Student, StudentNoID

router = APIRouter(prefix='/students', tags=['Students'])

# Model Pydantic = Datatype
class Student(BaseModel):
    id: str
    name: str

class StudentNoID(BaseModel):
    name: str

students = [
    Student(id="s1", name="Adama"),
    Student(id="s2", name="Adrien"),
    Student(id="ss3", name="Akbar")
]

# Verbs + Endpoints
@router.get('/', response_model=List[Student])
async def get_student():
    return students

# 1. Exercice (10min) Create new Student: POST
# response_model permet de définir de type de réponse (ici nous retournons le student avec sont id)
# status_code est défini sur 201-Created car c'est un POST
@router.post('/', response_model=Student, status_code=201)
async def create_student(givenName: StudentNoID):
    # génération de l'identifiant unique
    generatedId = str(uuid.uuid4())
    # création de l'object/dict Student
    newStudent = Student(id=generatedId, name=givenName.name)
    # Ajout du nouveau Student dans la List/Array
    students.append(newStudent)
    # Réponse définie par le Student avec son ID
    return newStudent

# 2. Exercice (10min) Student GET by ID
# response_model est un Student car nous souhaitons trouver l'étudiant correspondant à l'ID
@router.get('/{student_id}', response_model=Student)
async def get_student_by_ID(student_id: str):
    # On parcourt chaque étudiant de la liste
    for student in students:
        # Si l'ID correspond, on retourne l'étudiant trouvé
        if student.id == student_id:
            return student
    # Si on arrive ici, c'est que la boucle sur la liste "students" n'a rien trouvé
    # On lève donc un HTTP Exception
    raise HTTPException(status_code=404, detail="Student not found")

# 3. Exercice (10min) PATCH Student (name)
@router.patch('/{student_id}', status_code=204)
async def modify_student_name(student_id: str, modifiedStudent: StudentNoID):
    for student in students:
        if student.id == student_id:
            student.name = modifiedStudent.name
            return
    raise HTTPException(status_code=404, detail="Student not found")

# 4. Exercice (10min) DELETE Student
@router.delete('/{student_id}', status_code=204)
async def delete_student(student_id: str):
    for student in students:
        if student.id == student_id:
            students.remove(student)
            return
    raise HTTPException(status_code=404, detail="Student not found")

