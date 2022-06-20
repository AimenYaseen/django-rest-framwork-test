from rest_framework import serializers

from .models import User

# REGISTRATION SERIALIZER
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

# LOGIN SERIALIZER
class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField( max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


# USER CHANGE PASSWORD SERIALIZER
class UserEditProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True, required=False)
    password2 = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True, required=False)

    class Meta:
        fields=['name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        name = attrs.get('name')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm password should match with each other")
        user.set_password(password)
        user.name = name
        print(user.name)
        user.save()
        return attrs

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


# USER PROFILE SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']

# USER CHANGE PASSWORD SERIALIZER
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields=['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm password should match with each other")
        user.set_password(password)
        user.save()
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    post_set = serializers.PrimaryKeyRelatedField(many=True, read_only = True)
    
    class Meta:
        model=User
        fields = ['id', 'name', 'email', 'post_set']