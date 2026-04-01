from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

#import clasele
from proiect import engine, Identifier, Characteristic, IdentifierCharacteristic, get_db

# # import sesiunea DB
# from proiect import SessionLocal


app=FastAPI()

#test
# @app.get("/")
# def read_root():
#     return {"message": "hello fastapi"}

@app.get("/identifiers/")
def get_identifiers(db: Session = Depends(get_db)):
    #return [{"test": "merge"}]  # hardcodat temporar
    return db.query(Identifier).all()