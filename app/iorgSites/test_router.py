# import datetime
# import json
# import os
# from fastapi.testclient import TestClient
# import pytest
# from app.main import app
# from database import get_connection

# client = TestClient(app)
# test_iorgSites = [
#     {
#         "uid": "site-uuid-0001",
#         "createdByUid": "creator-uid-0001",
#         "dateCreated": datetime.datetime.now(),
#         "deleteFlag": False,
#         "complexName": "Complex A",
#         "companyName": "Company A",
#         "factoryManagementNumber": "FMN-001",
#         "addressRegionName": "Region A",
#         "addressLocality": "Locality A",
#         "postalCode": "12345",
#         "streetAddress": "1234 Street Name",
#         "landAddress": "Land Address A",
#         "businessRegistrationNum": "BRN-001",
#         "sectorIdMain": "1001",
#         "establishmentType": "Type A",
#         "propertyResidence": "General Land",
#         "propertyOwnership": "Owned",
#         "approvalDate": datetime.datetime.now(),
#         "registrationDate": datetime.datetime.now(),
#         "businessType": "Manufacturing",
#         "phoneNumber": "123-456-7890",
#         "products": "Product A, Product B",
#         "mainRawMaterials": "Material A, Material B",
#         "sizeCategory": "Medium",
#         "zoneType": "Industrial",
#         "landArea": 10000.0,
#         "manufacturingFacilityArea": 5000.0,
#         "dataSource": "DataSource A",
#         "keyHash": "unique-key-hash-0001",
#         "addressDetails": json.dumps({"detail": "value"}),
#     }
# ]

# @pytest.skip("Router testing not implemented")
# async def setup_db():
#     test_db_url = os.getenv("TEST_DATABASE_URL")
#     db_connection = get_connection()
#     db_connection._create_engine(test_db_url)
#     pytest.MonkeyPatch().setenv("DATABASE_URL", test_db_url)
#     await db_connection.connect()
#     yield   # This is where the test function will execute
#     await db_connection.disconnect()



# @pytest.skip("Router testing not implemented")
# def test_get():
#     response = client.get("/api/iorgSites")
#     assert (
#         response.status_code == 200
#     )  ##TODO: figure out how to prepare mock data for fastapi tests
