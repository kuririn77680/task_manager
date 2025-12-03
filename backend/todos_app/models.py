from django.db import models


class Todo(models.Model):
    STATUS_CHOICES = (
        ("TODO", "to do"),
        ("IN_PROGRESS", "in progress"),
        ("DONE", "done"),
    )

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    note = models.ForeignKey(
        "notes_app.Note",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="todos",
    )

    def __str__(self):
        return self.title
