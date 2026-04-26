
from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models import Customer,CustomerCreate, CustomerUpdate
from db import SessionDep

router = APIRouter()

@router.post('/customers',response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get('/customers', response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get('/customers/{id}',response_model=Customer)
async def get_customer(id: int, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    return customer

@router.patch('/customers/{id}',response_model=Customer, status_code=status.HTTP_201_CREATED)
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

@router.delete('/customers/{id}')
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    session.delete(customer)
    session.commit()
    return {'detail':'ok'}
    
