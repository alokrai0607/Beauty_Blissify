import pytest
# TestClient is used to simulate HTTP requests to the FastAPI app for testing.
from fastapi.testclient import TestClient
from app.main import app
from app import models, database

# Creates a TestClient instance for testing the FastAPI app. 
client = TestClient(app)

# Defines a dictionary with data for a test product. 
test_product_data = {
    "title": "TestProduct",
    "description": "Test product description",
    "category": "Test Category",
    "price": 1000.00,
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpgwRDsr8EUqh_FM8y-sdWQaj1dISjRRoj5xxtr9yqHkSI5BIkhvPYaAw&s"
}

#will set up the database for a test.
@pytest.fixture
def setup_db():
    #Creates a new database session .
    db = database.SessionLocal()
    # Creates a new instance of the Product
    new_product = models.Product(
        title=test_product_data["title"],
        description=test_product_data["description"],
        category=test_product_data["category"],
        price=test_product_data["price"],
        img=test_product_data["img"]
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    yield new_product
    # After the test is complete, this deletes the new_product entry from the database to clean up the test data.
    db.query(models.Product).filter(models.Product.id == new_product.id).delete()
    db.commit()

# 1. Testcase for POST prduct  
def test_create_product():
    response = client.post(
        "/api/v1/products/",
        json=test_product_data
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == test_product_data["title"]

# 2. Test for GET All Product  
def test_read_products():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 3. Test for GET api for any particular product by Product id
def test_read_product(setup_db):
    response = client.get(f"/api/v1/products/{setup_db.id}")
    assert response.status_code == 200
    assert response.json()["id"] == setup_db.id
    assert response.json()["title"] == setup_db.title

# 4. Test GET for non-existent product
def test_read_product_not_found():
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

# 5.  Test for patch api by id
def test_update_product(setup_db):
    updated_data = {
        "title": "Updated Title",
        "price": 149.99
    }
    response = client.patch(
        f"/api/v1/products/{setup_db.id}",
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["price"] == updated_data["price"]

# 6. Test PATCH api using id for non-existent product
def test_update_product_not_found():
    updated_data = {
        "title": "Non-existent Product"
    }
    response = client.patch("/api/v1/products/999999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

# 7. Test for PUT api by id
def test_replace_product(setup_db):
    replace_data = {
        "title": "Replaced Title",
        "description": "Replaced Description",
        "category": "Replaced Category",
        "price": 199.99,
        "img": "http://example.com/replaced-image.jpg"
    }
    response = client.put(
        f"/api/v1/products/{setup_db.id}",
        json=replace_data
    )
    assert response.status_code == 200
    assert response.json()["title"] == replace_data["title"]
    assert response.json()["description"] == replace_data["description"]

# 8. Test for DELETE api using id .
def test_delete_product(setup_db):
    response = client.delete(f"/api/v1/products/{setup_db.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Product deleted"

# 9. Test for DELETE api using id for non-existent product
def test_delete_product_not_found():
    response = client.delete("/api/v1/products/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
