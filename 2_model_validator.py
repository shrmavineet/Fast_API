from pydantic import BaseModel,EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Name of the patient which lenght is not more than 50 character', examples=['Vineet','Vivek'])]
    age: int = Field(gt=0, lt=120, default=18)
    email: EmailStr
    linkedin_url: AnyUrl
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Optional[bool] = None
    allergies: List[str]
    conact_details: Dict[str, str]
    emp_id: int


    # Model Validator
    @model_validator(mode='after')
    def validate_emergency(cls,model):
        if model.age > 60 and 'emergency' not in model.conact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(f'Patient Added in db')

patient_info = {'name':'Vineet', 'age':61,'emp_id':'51178', 'email':'abc@hdfcbank.com','linkedin_url':'https://linkedin.com/132' ,'weight': 75.2, 'allergies':['pollen', 'dust'], 'conact_details':{'contact_no':'1234567', 'emergency':'1234'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)