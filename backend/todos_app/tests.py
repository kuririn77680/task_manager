from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todos_app.models import Todo
from notes_app.models import Note


class TodoAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("todo-list")

    def test_create_todo_without_note_uses_default_status(self):
        payload = {"title": "Buy milk"}
        resp = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], payload["title"])
        # Default status should be "TODO"
        self.assertEqual(resp.data["status"], "TODO")
        self.assertIsNone(resp.data["note"])  # FK is nullable

    def test_create_todo_with_note(self):
        note = Note.objects.create(content="context")
        payload = {"title": "Do something", "note": note.pk}
        resp = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["note"], note.pk)

    def test_list_and_retrieve_todos(self):
        t1 = Todo.objects.create(title="t1")
        t2 = Todo.objects.create(title="t2")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
        # retrieve first
        detail_url = reverse("todo-detail", args=[t1.pk])
        r2 = self.client.get(detail_url)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data["id"], t1.pk)
        self.assertEqual(r2.data["title"], t1.title)

    def test_update_title_and_status(self):
        todo = Todo.objects.create(title="initial")
        detail_url = reverse("todo-detail", args=[todo.pk])
        # valid status
        r_ok = self.client.patch(
            detail_url,
            data={"title": "updated", "status": "IN_PROGRESS"},
            format="json",
        )
        self.assertEqual(r_ok.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.title, "updated")
        self.assertEqual(todo.status, "IN_PROGRESS")

        # invalid status should be rejected by serializer validation
        r_bad = self.client.patch(detail_url, data={"status": "INVALID"}, format="json")
        self.assertEqual(r_bad.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reassign_note_and_delete(self):
        note1 = Note.objects.create(content="n1")
        note2 = Note.objects.create(content="n2")
        todo = Todo.objects.create(title="t", note=note1)
        detail_url = reverse("todo-detail", args=[todo.pk])
        # reassign FK
        r = self.client.patch(detail_url, data={"note": note2.pk}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.note_id, note2.pk)

        # delete
        r_del = self.client.delete(detail_url)
        self.assertEqual(r_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())
