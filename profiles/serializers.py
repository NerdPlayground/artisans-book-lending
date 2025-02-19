from .models import Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=["banned"]

class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()

    class Meta:
        model=get_user_model()
        fields=['username','first_name','last_name','email','profile']
    
    def update(self,instance,validated_data):
        profile=Profile.objects.get(user=instance)
        profile_data=validated_data.get("profile")
        profile.banned=profile_data["banned"]
        profile.save()

        instance.username=validated_data["username"]
        instance.first_name=validated_data["first_name"]
        instance.last_name=validated_data["last_name"]
        instance.email=validated_data["email"]
        instance.save()

        return instance