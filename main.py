import zoneinfo

from datetime import datetime

from fastapi import FastAPI

from models import CustomerCreate,Customer, Transaction, Invoice

    

app = FastAPI()

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
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    ## Asumiendo que se hace en bd
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get('/customers', response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get('/customers/{id}',response_model=Customer)
async def get_customer(id: int):
    return db_customers.__getitem__(id)

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data

