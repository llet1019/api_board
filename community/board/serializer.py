from rest_framework import serializers

from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            'id', 'category_id', 'user_id', 'context', 'view_cnt', 'created_at', 'updated_at'
        ]