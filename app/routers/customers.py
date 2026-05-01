
from fastapi import APIRouter, Query, status, HTTPException
from sqlmodel import select

from models import Customer,CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum
from db import SessionDep

router = APIRouter(tags=['customers'])

@router.post(
    '/customers',
    response_model=Customer,
    status_code=status.HTTP_201_CREATED
    )
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

@router.patch('/customers/{id}',response_model=Customer, status_code=status.HTTP_200_OK)
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

@router.delete('/customers/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer,id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    session.delete(customer)
    session.commit()
    return {'detail':'ok'}
    
@router.post('/customers/{customer_id}/plans/{plan_id}')
async def subscribe_customer_to_plan(customer_id: int,plan_id: int,session: SessionDep ,plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer,customer_id)
    plan_db = session.get(Plan,plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The customer or plan doesnt exist'
        )
    
    customer_plan_db =CustomerPlan(plan_id=plan_db.id,customer_id=customer_db.id,status=plan_status)
    
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get('/customers/{customer_id}/plans/')
async def get_subscriptions(customer_id: int ,session: SessionDep, plan_status: StatusEnum = Query()):
    customer = session.get(Customer,customer_id)
    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Customer not found')
    query = select(CustomerPlan).where(CustomerPlan.customer_id==customer_id).where(CustomerPlan.status== plan_status)
    plans = session.exec(query).all()
    return plans