import time
import zoneinfo

from datetime import datetime

from db import create_all_tables

from fastapi import FastAPI, Request

from models import  Transaction, Invoice
from .routers import customers, transactions, plans
    

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    
    start_time= time.time() 
    response = await call_next(request) 
    process_time = time.time() - start_time
    print(f'Request: {request.url} completed in:{process_time:.4f} seconds')
    return response

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
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}


@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data

