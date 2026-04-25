import zoneinfo

from datetime import datetime

from db import SessionDep, create_all_tables

from fastapi import FastAPI, HTTPException, status

from models import CustomerCreate,Customer, CustomerUpdate, Transaction, Invoice
from sqlmodel import select
    

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {'message':"hola"}

country_timezones = {
    'CO': 'America/Bogota',
    'MX': 'America/Mexico_City',
    'AR': 'America/Argentina/Buenos_Aires',
    'BR': 'America/Sao_Paulo',
    'PE': 'America/Lima'
}

@app.get('/time/{iso_code}')
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

db_customers: list[Customer] = []
current_id: int = 0

@app.post('/customers',response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get('/customers', response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get('/customers/{id}',response_model=Customer)
async def get_customer(id: int, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    return customer

@app.patch('/customers/{id}',response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.delete('/customers/{id}')
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    session.delete(customer)
    session.commit()
    return {'detail':'ok'}
    


@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data

