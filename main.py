from fastapi import FastAPI,Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):
    id: Annotated[int, Field(...,description='Patient Id to make uniqueness', examples=[123])]
    name: Annotated[str, Field(...,description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., description='Current age of the patient as per the dob on aadhar',)]
    gender: Annotated[Literal['male', 'female'], Field(default='undefined',description='Gender of the patient')]
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

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal['male', 'female']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

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
    patient = data.get(str(patientid))

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "id": patientid,
        **patient
    }


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

@app.put("/update_patient/{patient_id}")
def update_patinent_work(patient_id: int, patient_update: PatientUpdate)-> str:
    data = load_jsondata()
    if str(patient_id) not in data:
        raise HTTPException(status_code=404, detail='Patient not Found')
    existing_record = data[str(patient_id)]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_record[key] = value

    # existing_patient_info -> pydantic object -> update bmi + verdict -> pydantic object -> dic
    existing_record['id'] = patient_id
    patient_pydatic_object = Patient(**existing_record)

    # -> pydantic object -> dict
    existing_record = patient_pydatic_object.model_dump(exclude='id')

    # add this dict to data
    data[str(patient_id)] = existing_record

    #save data
    save_data(data) 

    return JSONResponse(status_code=200, content={'message':"Patient Updated Successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:int):
    #load_data
    data = load_jsondata()
    if str(patient_id) not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[str(patient_id)]
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'patient deleted'})