from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ["content", "todos"]
