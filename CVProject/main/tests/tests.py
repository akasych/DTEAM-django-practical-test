from django.test import TestCase
from ..models import CVDoc, Skill


class TestListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        CVDoc.objects.create(firstname="John", lastname="Smith", email="john@smith")
        CVDoc.objects.create(firstname="Sara", lastname="Brown", email="sara@brown")

    def test_template_file(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "index.html")

    def test_page_breadcrumb(self):
        response = self.client.get("/")
        self.assertContains(response, "List CVs")

    def test_page_list_names(self):
        response = self.client.get("/")
        self.assertContains(response, "John Smith")
        self.assertContains(response, "Sara Brown")

    def test_page_context_i18n(self):
        response = self.client.get("/")
        self.assertGreater(len(response.context['bundles']), 0)
        self.assertIn('curr_lang', response.context.keys())


class TestDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cv = CVDoc.objects.create(firstname="John", lastname="Smith", email="john@smith", phone="123456")
        Skill.objects.create(cvDoc_id=cls.cv.id, title="Python", experience="3")

    def test_template_file(self):
        response = self.client.get(f"/cv/{self.cv.id}/")
        self.assertTemplateUsed(response, "cv.html")

    def test_page_breadcrumb(self):
        response = self.client.get(f"/cv/{self.cv.id}/")
        self.assertContains(response, "CV Profile - John Smith")

    def test_page_list_details(self):
        response = self.client.get(f"/cv/{self.cv.id}/")
        self.assertContains(response, "John Smith")
        self.assertContains(response, "john@smith")
        self.assertContains(response, "123456")

    def test_page_list_skills(self):
        response = self.client.get(f"/cv/{self.cv.id}/")
        self.assertContains(response, "Python: 3 years")

