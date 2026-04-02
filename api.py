from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

#import clasele
from proiect import Country, CountrySchema, IdentifierSchema, engine, Identifier, Characteristic, IdentifierCharacteristic, get_db
from proiect import IdentifierCreate,IdentifierUpdate, CountryCreate, CountryUpdate
from fastapi.middleware.cors import CORSMiddleware
# # import sesiunea DB
# from proiect import SessionLocal


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau ["http://127.0.0.1:5500"] 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#test
# @app.get("/")
# def read_root():
#     return {"message": "hello fastapi"}

@app.get("/")
def root():
    return {"message": "FastApi -> proiect"}

@app.get("/identifiers/")
def get_identifiers(db: Session = Depends(get_db)):
    #return [{"test": "merge"}]  # hardcodat temporar
    return db.query(Identifier).all()

@app.get("/identifiers/{identifier_name}", response_model=IdentifierSchema)
def read_identifier(identifier_name: str, db: Session = Depends(get_db)):
    identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    return identifier

@app.post("/identifiers/", response_model=IdentifierSchema)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    existing = db.query(Identifier).filter(
        Identifier.identifier_name == identifier.identifier_name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Identifier already exists")

    db_identifier = Identifier(**identifier.model_dump())
    db.add(db_identifier)
    db.commit()
    db.refresh(db_identifier)
    return db_identifier


@app.put("/identifiers/{identifier_name}", response_model=IdentifierSchema)
def update_identifier(identifier_name: str, identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    for key, value in identifier.model_dump().items():
        setattr(db_identifier, key, value)

    db.commit()
    db.refresh(db_identifier)
    return db_identifier


@app.patch("/identifiers/{identifier_name}", response_model=IdentifierSchema)
def patch_identifier(identifier_name: str, identifier_update: IdentifierUpdate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    update_data = identifier_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_identifier, key, value)

    db.commit()
    db.refresh(db_identifier)
    return db_identifier


@app.delete("/identifiers/{identifier_name}")
def delete_identifier(identifier_name: str, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    db.delete(db_identifier)
    db.commit()
    return {"detail": "Identifier deleted"}




@app.get("/countries/", response_model=list[CountrySchema])
def read_all_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()


@app.get("/countries/{country_name}", response_model=CountrySchema )
def read_country(country_name: str, db: Session = Depends(get_db)):
    country = db.query(Country).filter(
        Country.name == country_name
    ).first()

    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    return country


@app.post("/countries/", response_model=CountrySchema)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    existing = db.query(Country).filter(
        Country.name == country.name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Country already exists")

    db_country = Country(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


@app.patch("/countries/{country_name}", response_model=CountrySchema)
def patch_country(country_name: str, country_update: CountryUpdate, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(
        Country.name == country_name
    ).first()

    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    update_data = country_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_country, key, value)

    db.commit()
    db.refresh(db_country)
    return db_country


@app.delete("/countries/{country_name}")
def delete_country(country_name: str, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(
        Country.name == country_name
    ).first()

    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(db_country)
    db.commit()
    return {"detail": "Country deleted"}
