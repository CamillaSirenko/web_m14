from fastapi import Depends, HTTPException, status, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database.models import Contact 
from src.database.db import get_db
from src.schemas import ContactCreateUpdate, ContactResponse
from typing import List
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import extract
from src.services.auth import auth_service


router = APIRouter()

 
@router.post("/contacts/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreateUpdate,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.get_current_user)
):
    """
    The create_contact function creates a new contact in the database.
    
    :param contact: ContactCreateUpdate: Create a new contact
    :param db: Session: Pass in the database session
    :param current_user: Contact: Get the current user
    :return: A contactresponse object
    :doc-author: Trelent
    """
    db_contact = Contact(**contact.dict(), user_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return ContactResponse(**db_contact.__dict__)

@router.get("/upcoming_birthdays/", response_model=List[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    """
    The upcoming_birthdays function returns a list of contacts whose birthdays are within the next week.
    
    
    :param db: Session: Get the database session
    :return: A list of contactresponse objects,
    :doc-author: Trelent
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    contacts = db.query(Contact).filter(
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= next_week.day
    ).all()

    return [ContactResponse(**contact.__dict__) for contact in contacts]

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.get_current_user)
):
    """
    The get_contact function returns a single contact from the database.
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get a database session
    :param current_user: Contact: Get the current user
    :return: A contactresponse object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse(**contact.__dict__)

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactCreateUpdate,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.get_current_user)
):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - contact_id: int, the id of the contact to be updated.
            - contact: ContactCreateUpdate, an object containing all of the fields that can be updated for a given user. 
                This is defined in schemas/contact_create_update.py and contains firstname, lastname, email and phone number fields
                as well as their corresponding validators (see schemas/validators).
            - db: Session = Depends(get_db), this is an SQLAl
    
    :param contact_id: int: Identify the contact that we want to update
    :param contact: ContactCreateUpdate: Pass the contact data to the function
    :param db: Session: Access the database
    :param current_user: Contact: Get the current user from the database
    :return: A contactresponse object
    :doc-author: Trelent
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return ContactResponse(**db_contact.__dict__)

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: Contact = Depends(auth_service.get_current_user)
):
    """
    The delete_contact function deletes a contact from the database.
    
    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: Contact: Get the current user
    :return: A contactresponse object
    :doc-author: Trelent
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return ContactResponse(**db_contact.__dict__)
