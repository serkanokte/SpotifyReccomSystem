from collections import Counter
import pandas as pd 
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework.response import Response
from tracks.models import Track, TrackUserModel
from rest_framework import status


def create_pivot_dataframe(target_ratings):
    
    df = pd.DataFrame.from_records(target_ratings.values('User', 'Track', 'rating'))
    
    pivot_df = df.pivot(index='User', columns='Track', values='rating')
    

    return pivot_df



## Şarkılarrın ve Kullanıcıların Rating ortalamalarının alınması
def get_track_avg_ratings(track_ids, user_ids):
    track_avg_ratings = []
    for track_id in track_ids:
        track_ratings = TrackUserModel.objects.filter(Track__id=track_id, User__id__in=user_ids)
        avg_rating = track_ratings.aggregate(Avg('rating'))['rating__avg']
        track_avg_ratings.append({'track_id': track_id, 'avg_rating': avg_rating})
    return track_avg_ratings








def recommend_tracks(closest_users_top10_list, track_ids,user_object):
    
    total = 0
    besttracks = []
    
    if len(closest_users_top10_list) != 0:
        #en çok benzeyen kullanıcıların 4 puan üstü verdiği şarkıları alma
        tracks_queryset = TrackUserModel.objects.filter(User__in=closest_users_top10_list, rating__gte=4.0).exclude(Track__in=track_ids)
        
        
        all_tracks = [track.Track_id for track in tracks_queryset]
        
        track_counts = Counter(all_tracks)
        
        grouped_tracks = {}
        
        for track_id, count in track_counts.items():
            if count not in grouped_tracks:
                grouped_tracks[count] = [track_id]
            else:
                grouped_tracks[count].append(track_id)
        
        
        
        result_list = [grouped_tracks[key] for key in sorted(grouped_tracks.keys(), reverse=True)]

        

        ## 20 öneri olana besttracks'a şarkıları ekleme
        for result in result_list:
            if total < 20:
                
                if total + len(result) < 20:
                    total += len(result)
                    besttracks.extend(result)
                else:
                    ## eğer eşit sayıda kullanıcı tarafından 4 üstü puan alınmışsa 
                    #benzer kullanıcıların o şarkıya verdiği puanların ortalamasına göre öneri yapılması
                    need_track_count = 20 - total
                    track_avg_ratings = get_track_avg_ratings(result, closest_users_top10_list)
                    sorted_track_avg_ratings = sorted(track_avg_ratings, key=lambda x: x['avg_rating'], reverse=True)
                    besttracks.extend(entry['track_id'] for entry in sorted_track_avg_ratings[:need_track_count])
                    total = 20
    #Eğer Üstteki işlemlere rağmen 20 şarkı değerine ulaşılamamışsa 
    #kullanıcının en çok beğendiği şarkı türüne göre Spotifyden sağlanan popularity ile öneri sunulması

    print(total)     
                      
    if total < 20:

        ## şarkıların alınması
        need=20-total
        
        track_user = TrackUserModel.objects.filter(Track__id__in=track_ids,User=user_object,rating__gte=4.0)
        
        track_user_ids = track_user.values_list('Track_id',flat=True)
        
        tracks= Track.objects.filter(id__in=track_user_ids)
        if(total > 4 and track_user.count() < 1):
            return besttracks
        ## eğer kullanıcı 1 adet bile 4.0 üstü puan vermemişse hata verme
        if(track_user.count() < 1):
            
            return None


        
        ## En popüler şarkı türlerini 4.0 puan sayısına göre alma işlemi
        genre_list = [] 
        for track in tracks:
            genre_list.append(track.genres)
        

        most_genres= Counter(genre_list).most_common()
        ## Kullanıcının en iyi bulduğu türün önceden puan verdiği şarkıların haricindeki şarkılarının alınıp Spotify'ın sağladığı popularitye göre sıralanması 
        tracks_que = Track.objects.filter(genres=most_genres[0][0]).exclude(id__in=track_ids).order_by('-popularity')[:need]


        for track in tracks_que:
            besttracks.append(track.id)


    return besttracks




def euclidean_distance(row, selected_track_data):
    return (((row - selected_track_data)**2).sum())**0.5