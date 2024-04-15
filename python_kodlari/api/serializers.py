from rest_framework import serializers
from tracks.models import Track,TrackUserModel
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id','name','genres','artist']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation']

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise serializers.ValidationError("Şifre ve şifre onayi eşleşmiyor.")
        
        if len(password) < 8:
            raise serializers.ValidationError("Şifre en az 8 karakter uzunluğunda olmalidir.")

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user



class  SimilarTrackSerializer(serializers.Serializer):

    id = serializers.CharField()
    name = serializers.CharField()
    artist = serializers.CharField()
    genres = serializers.CharField()
    euclidean_distance = serializers.FloatField()





class TrackRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name','genres','artist']





class UserTrackListSerializer(serializers.ModelSerializer):
    track = TrackRateSerializer(source='Track', read_only=True)
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.User.username

    class Meta:
        model = TrackUserModel
        fields = ['user_name', 'track', 'rating']



class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackUserModel
        fields = ('rating',)



class UserLoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    


class TrackUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackUserModel
        fields = ['User','Track','rating']





