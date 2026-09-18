from fastapi import FastAPI,Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated
import json

class Patient(BaseModel):
    id: Annotated[int, Field(...,description='Patient Id to make uniqueness', examples=[123])]
    name: Annotated[str, Field(...,description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., description='Current age of the patient as per the dob on aadhar',)]
    gender: Annotated[str, Field(default='Non-define',description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meter")]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        else:
            return 'Overweight'

def load_jsondata():
    with open('pstient.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('pstient.json', 'w') as f:
        json.dump(data,f)


app = FastAPI()

@app.get("/")
def hello():
    return { 'message': "Hello World!"}


@app.get("/about")
def about_page():
    return {'message': 'This is the about page which contain the details'}


@app.get("/view")
def view_data():
    data = load_jsondata()
    return data

@app.get("/patient/{patientid}")
def single_patient(patientid: int =Path(..., description="Id of the patient in the DB",example=27)):
    data = load_jsondata()
    for patient in data:
        if patient["id"] == patientid:
            return patient
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patient(sort_by: str=Query(...,description='Sort on the basis of publication_date, filing_date'), order: str=Query('asc',description='sort in asc or desc order')):
    valid_fields = ['publication_date', 'filing_date']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_jsondata()
    sort_order = True if order =='desc' else False

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, ''),
        reverse=sort_order
    )
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_jsondata()

    #check if the patient already exits
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # new patient add to the db

    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient created successfully'})