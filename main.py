from fastapi import FastAPI,Path, HTTPException, Query
import json


def load_jsondata():
    with open('pstient.json','r') as f:
        data = json.load(f)

    return data


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