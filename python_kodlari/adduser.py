import os
import django
import random
from faker import Faker
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","musicsystem.settings")
django.setup()


from django.contrib.auth.models import User
from tracks.models import TrackUserModel,Track


if __name__ == '__main__':

    fake = Faker()

    for i in range(0,700):
            
            fake_name = f'{fake.first_name()}{i}'
            
            new_user = User.objects.create_user(username=fake_name, password='password123')
            print(i)


    for i in range(35000):
        user = User.objects.order_by('?').first()
        track = Track.objects.order_by('?').first() 
        rating = random.randint(1, 10)
        rating = rating / 2.0
        existing_track_user = TrackUserModel.objects.filter(User=user, Track=track).first()

        if existing_track_user:

            existing_track_user.rating = rating
            existing_track_user.save()
            print(f"{i} Rating guncellendi")

        else:
            
            new_track_user = TrackUserModel(User=user, Track=track, rating=rating)
            new_track_user.save()
            print(f"{i} yeni model eklendi")