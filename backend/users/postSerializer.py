from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Post
        fields = '__all__'

        # fields = ['id', 'title', 'body', 'created_at', 'owner']

    # def update(self, instance, validated_data):
    #     instance.save()
    #     return super().update(instance, validated_data)

