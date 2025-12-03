from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notes_app.models import Note
from todos_app.models import Todo


class NoteAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("note-list")

    def test_create_note(self):
        payload = {"content": "My first note"}
        resp = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["content"], payload["content"])
        # 'todos' is read-only and should be present as an empty list on creation
        self.assertIn("todos", resp.data)
        self.assertEqual(resp.data["todos"], [])
        self.assertEqual(Note.objects.count(), 1)

    def test_list_notes(self):
        Note.objects.create(content="n1")
        Note.objects.create(content="n2")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_retrieve_note_includes_related_todos(self):
        note = Note.objects.create(content="with todos")
        # create a couple of todos linked to the note
        t1 = Todo.objects.create(title="t1", note=note)
        t2 = Todo.objects.create(title="t2", note=note)
        detail_url = reverse("note-detail", args=[note.pk])
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # ensure 'todos' contains the primary keys
        self.assertIn("todos", resp.data)
        self.assertCountEqual(resp.data["todos"], [t1.pk, t2.pk])

    def test_update_note(self):
        note = Note.objects.create(content="old")
        detail_url = reverse("note-detail", args=[note.pk])
        resp = self.client.patch(detail_url, data={"content": "new"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.content, "new")

    def test_delete_note(self):
        note = Note.objects.create(content="to delete")
        detail_url = reverse("note-detail", args=[note.pk])
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())
