from rest_framework import serializers

from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Adding Extra Field
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    # Automatically generate fields and do validations 
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password':{'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password should match with each other")
        return attrs

    # creating the user
    def create(self, validated_data):
        # return super().create(validated_data)
        return User.objects.create_user(**validated_data)
