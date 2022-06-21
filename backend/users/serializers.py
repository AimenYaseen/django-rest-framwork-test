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
        email = validated_data['email']
        name = validated_data['name']
        password = validated_data['password']

        return User.objects.create_user(email=email, name=name, password=password)

# LOGIN SERIALIZER
class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField( max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


# USER EDIT PROFILE SERIALIZER
class UserEditProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True, required=False)
    password2 = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True, required=False)
    old_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields=['name', 'password', 'password2', 'old_password']

    def validate(self, attrs):
        password = attrs.get('password')
        print(password)
        password2 = attrs.get('password2')
        print(password2)
        user = self.context.get('user')
        name = attrs.get('name')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm password should match with each other")
        
        if name is not None:
           user.name = name
        if password is not None:
           user.set_password(password)
           print(user.name)

        user.save()
        return attrs

    def validate_old_password(self, value):
        user = self.context.get('user')
        print(user.check_password(value))
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value
    
    # def update(self, instance, validated_data):
    #     user = self.context.get('user')
      
    #     # if validated_data['password'] is not None:
    #     user.set_password(validated_data['password'])

    #     # if validated_data['name'] is not None:
    #     user.name = validated_data['name']
    #     print(user.name)

    #     user.save()

        # return user


# FOR ANONYMOUS USER PROFILE SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']

# USER PROFILE SERIALIZER
class UserProfileSerializer(serializers.ModelSerializer):
    post_set = serializers.PrimaryKeyRelatedField(many=True, read_only = True)
    
    class Meta:
        model=User
        fields = ['id', 'name', 'email', 'post_set']

# # USER CHANGE PASSWORD SERIALIZER
# class UserChangePasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(max_length=20, min_length=8,style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         fields=['password', 'password2']

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         user = self.context.get('user')

#         if password != password2:
#             raise serializers.ValidationError("Password and Confirm password should match with each other")
#         user.set_password(password)
#         user.save()
#         return attrs

