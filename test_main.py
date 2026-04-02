# from fastapi.testclient import TestClient
# from api import app
# client = TestClient(app)


# # verifica daca endpointul "/" functioneaza corect 
# def test_root():
#     response = client.get("/") #like e echivalent cu deschiderea manuala in browser
#     print(response.status_code)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json() == {"message": "FastApi -> proiect"}  # daca imi arata 200 atunci it works



# def test_get_all_identifiers():  #dă-mi toate identificatoarele din sistem
#     response = client.get("/identifiers/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#    #isinstance -> x e de tip lista?


# # #Pot să iau un identifier specific după nume și API-ul îmi returnează corect acel obiect.
# # def test_get_identifier_by_name():
# #     response = client.get("/identifiers/99999999")
# #     assert response.status_code == 200
# #     assert response.json()["identifier_name"] == "99999999"




# def test_create_country():
#     response = client.post("/countries/", json={
#         "name": "Spain",
#         "iso_code": "ES",
#         "short_code": "724"
#     })

#     assert response.status_code == 200
#     assert response.json()["name"] == "Spain"
#     assert response.json()["iso_code"] == "ES"
#     assert response.json()["short_code"] == "724"




# def test_get_country_by_name():
#     response = client.get("/countries/Spain")
#     assert response.status_code == 200
#     assert response.json()["name"] == "Spain"




# def test_get_missing_country():
#     response = client.get("/countries/UnknownCountry")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Country not found"}

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

test_identifier = {
    "identifier_name": "ID_001",
    "description": "Test Description"
}

def test_create_identifier():
    response = client.post("/identifiers/", json=test_identifier)
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "ID_001"

def test_create_duplicate_identifier():
    # Încercăm să creăm același identificator a doua oară
    response = client.post("/identifiers/", json=test_identifier)
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifier already exists"

def test_get_all_identifiers():
    response = client.get("/identifiers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_identifier():
    response = client.get(f"/identifiers/{test_identifier['identifier_name']}")
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "ID_001"

def test_patch_identifier():
    patch_data = {"description": "Updated Description"}
    response = client.patch(f"/identifiers/{test_identifier['identifier_name']}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Description"

def test_delete_identifier():
    response = client.delete(f"/identifiers/{test_identifier['identifier_name']}")
    assert response.status_code == 200
    # Verificăm dacă a fost într-adevăr șters
    get_response = client.get(f"/identifiers/{test_identifier['identifier_name']}")
    assert get_response.status_code == 404

@pytest.fixture
def temp_country():
    # SETUP: Cream o tara specifica pentru test
    name = "Test_Fixture_Country"
    client.post("/countries/", json={"name": name})
    
    yield name  # Aici testul primeste numele si ruleaza
    
    # TEARDOWN: Dupa ce testul se termina (indiferent daca trece sau pica), stergem tara
    client.delete(f"/countries/{name}")

def test_read_country(temp_country):
    # temp_country este string-ul "Test_Fixture_Country"
    response = client.get(f"/countries/{temp_country}")
    assert response.status_code == 200

# def test_create_country():
#     country_data = {"name": "Romania", "code": "RO"} # Ajustează conform schemei tale
#     response = client.post("/countries/", json=country_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Romania"

def test_read_non_existent_country():
    response = client.get("/countries/Atlantis")
    assert response.status_code == 404