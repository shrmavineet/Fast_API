from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pincode: int

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_dict = {'city':'Noida', 'state':'Uttar Pradesh', 'pincode': 201301}

addr = Address(**address_dict)

details = {
    'name': 'Vineet',
    'age': 22,
    'address': addr
}

patient_details = Patient(**details)

print(patient_details)


temp = patient_details.model_dump() #convert into dictonary 
temp_json = patient_details.model_dump_json() 
print(temp)
print(type(temp))
