from pydantic import BaseModel,EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Name of the patient which lenght is not more than 50 character', examples=['Vineet','Vivek'])]
    age: int = Field(gt=0, lt=120, default=18)
    email: EmailStr
    linkedin_url: AnyUrl
    weight: Annotated[float, Field(gt=0, strict=True)] #in kg
    height:float = Field(gt=1) # in meter
    married: Optional[bool] = None
    allergies: List[str]
    conact_details: Dict[str, str]
    emp_id: int

    @computed_field
    @property
    def bmi(self)-> float:
        return round(self.weight/(self.height**2),2)

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print(f'Patient Added in db')

patient_info = {'name':'Vineet', 'age':30,'emp_id':'51178', 'email':'abc@hdfcbank.com','linkedin_url':'https://linkedin.com/132' ,'weight': 75.2, 'height': 1.75, 'allergies':['pollen', 'dust'], 'conact_details':{'contact_no':'1234567'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)