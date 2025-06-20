from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient
from ..models import CVDoc


class TestAPI(APITestCase):
    def setUp(self):
        self.client = RequestsClient()
        self.cv = CVDoc.objects.create(firstname="John", lastname="Smith", email="john@smith")

    def test_retrieve_data(self):
        response = self.client.get('http://testserver/api/cv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"id":1,"skills":[],"projects":[],"total_experience":0,"firstname":"John","lastname":"Smith","email":"john@smith","phone":"","profession":"","avatar":null}]')

    def test_create_data(self):
        response = self.client.post(url='http://testserver/api/add/', json={
            "firstname": "Bob",
            "lastname": "Lord",
            "email": "bob@lord",
            "phone": "",
            "profession": "Test Engineer",
            "skills": [],
            "projects": []
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_data(self):
        response = self.client.put(url=f'http://testserver/api/cv/{self.cv.id}', json={
            "firstname": "John_UPD",
            "lastname": "Smith",
            "email": "john@smith",
            "phone": "123",
            "profession": "Software Engineer",
            "skills": [],
            "projects": []
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_cv = CVDoc.objects.get(id=1)
        self.assertEqual(updated_cv.firstname, "John_UPD")
        self.assertEqual(updated_cv.phone, "123")
        self.assertEqual(updated_cv.profession, "Software Engineer")

    def test_delete_data(self):
        response = self.client.delete(url=f'http://testserver/api/cv/{self.cv.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(CVDoc.DoesNotExist, CVDoc.objects.get, id=self.cv.id)
