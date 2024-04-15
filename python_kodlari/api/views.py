import time
from rest_framework.response import Response
from rest_framework import generics,status
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from tracks.models import Track,TrackUserModel
from tracks.api.paginator import CustomPageNumberPagination
from tracks.api.serializers import RateSerializer, TrackSerializer,SimilarTrackSerializer, TrackUserModelSerializer, UserSerializer,UserTrackListSerializer,UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from tracks.func import create_pivot_dataframe,recommend_tracks,euclidean_distance
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score




class TrackListView(generics.ListAPIView):
      
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

   
    
    



class ListTrackByGenres(generics.ListAPIView):
    serializer_class = TrackSerializer


    def get_queryset(self):
        genres = self.kwargs.get('genres')
        
        queryset = Track.objects.filter(genres__iexact=genres) 

        return queryset
    






class ListTrackByArtist(generics.ListAPIView):
    serializer_class = TrackSerializer

    def list(self, request, *args, **kwargs):
        artist_name = self.kwargs.get('artist')
        
        
        
        queryset = Track.objects.filter(artist__iexact=artist_name)
        
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)
    



###Pearson Correlation
    
class ListSimilarUserReccom(generics.ListAPIView):
    serializer_class=TrackSerializer
    queryset=Track.objects.all()

    def list(self, request, *args, **kwargs):
            
            user_obj= request.user
            
            target_user_ratings=TrackUserModel.objects.filter(User=user_obj)
            
            ## en az 10 yorum isteme
            if target_user_ratings.count() < 10:
                return Response({'error': 'Yetersiz degerlendirme sayisi.'}, status=status.HTTP_400_BAD_REQUEST)
            

            target_users_trackids=target_user_ratings.values_list('Track_id', flat=True)

            ##Ortak şarkılı kullanıcıların ratingleriyle alınması
            other_users = TrackUserModel.objects.filter(Track__in=target_users_trackids).exclude(User=user_obj)
            

            

            ##### 5 ve üstünde ortak şarkısı olan kullanıcıların listesi
            other_users = other_users.values(
                'User'
            ).annotate(
                same_tracks=Count('Track')
            ).filter(
                same_tracks__gte=5
            ).order_by('-same_tracks')

            
            
            pivot_df_target_user=create_pivot_dataframe(target_user_ratings)
            
            std_pivot = pivot_df_target_user.std(axis=1)
            
            
                
            
            

            other_users_ratings=TrackUserModel.objects.filter(User__in=other_users.values('User'))
            
            if len(other_users_ratings) != 0:
                
                pivot_df_other_users = create_pivot_dataframe(other_users_ratings)
                
                # Eğer Asıl Kullanıcı her şarkıya aynı puanı vermemişse Pearson uygulamak
                if std_pivot.iloc[0] != 0:
                    pivot_df_other_users = pivot_df_other_users.sub(pivot_df_other_users.mean(axis=1), axis=0)
                    pivot_df_target_user = pivot_df_target_user.sub(pivot_df_target_user.mean(axis=1),axis=0)
                    

                # eksik sütunları ekleme işlemi
                columns_user = pivot_df_target_user.columns
                
                missing_columns = [col for col in columns_user if col not in pivot_df_other_users.columns]
                
                for col in missing_columns:
                    pivot_df_other_users[col] = 0
                


                pivot_df_other_users=pivot_df_other_users[columns_user]
                

                
                pivot_df_target_user=pivot_df_target_user.sort_index(axis=1)
                pivot_df_other_users=pivot_df_other_users.sort_index(axis=1)
                
                
                
                pivot_df_other_users=pivot_df_other_users.fillna(0)
                            
                ### cos similarity
                

                norms=(np.linalg.norm(pivot_df_target_user, axis=1) * np.linalg.norm(pivot_df_other_users, axis=1))
                norms=np.where(norms == 0, -1, norms)
                dot=np.dot(pivot_df_target_user, pivot_df_other_users.T)
                
                
                cos_sim=dot/norms

                
                #pearson correlation sonucu negatif ilişkisi olanları eleme
                index_pivdf=pivot_df_other_users.index
                user_cos_sim_dict = dict(zip(index_pivdf, cos_sim[0]))

                user_cos_sim_dict = {user_id: sim_score for user_id, sim_score in user_cos_sim_dict.items() if sim_score >= 0}
                
                
                    
                ### en yakın 10 kullanıcıyı alma işlemi
                sorted_users = sorted(user_cos_sim_dict.items(), key=lambda x: x[1], reverse=True)[:10]
                
                user_ids=[users[0] for users in sorted_users]

                
                #####şarkı önerisi
                reccomTrack=recommend_tracks(user_ids,target_users_trackids,user_object=user_obj)
                
                if reccomTrack is None:
                    return Response({'error': 'En az 1 tane 4 puan ustu sarki gerekli.'}, status=status.HTTP_400_BAD_REQUEST)
                
                recommended_tracks_info = sorted(Track.objects.filter(id__in=reccomTrack).values('id', 'name', 'genres', 'artist'), key=lambda x: reccomTrack.index(x['id']))

                serializer = self.get_serializer(recommended_tracks_info, many=True)

                serialized_data = serializer.data
                
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                
                reccomTrack=recommend_tracks(other_users_ratings,target_users_trackids,user_object=user_obj)

                if reccomTrack is None:
                    return Response({'error': 'En az 1 tane 4 puan ustu sarki gerekli.'}, status=status.HTTP_400_BAD_REQUEST)
                else:   
                    recommended_tracks_info = sorted(Track.objects.filter(id__in=reccomTrack).values('id', 'name', 'genres', 'artist'), key=lambda x: reccomTrack.index(x['id']))

                    serializer = self.get_serializer(recommended_tracks_info, many=True)

                    serialized_data = serializer.data

                    return Response(serialized_data, status=status.HTTP_200_OK)

            


class SimilarTrackListView(generics.ListAPIView):

    serializer_class = SimilarTrackSerializer
    queryset = Track.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            # start_time = time.time()
            track_id = self.kwargs.get('track_id')     

            k = self.kwargs.get('k')
            queryset = self.get_queryset()
            
            

            df_all = pd.DataFrame.from_records(queryset.values())
            
            
            df_all.set_index('id',inplace=True)

#####onehotencoding            
            # track_genres = df_all.loc[track_id, 'genres']

            # genres_set = {'Blues', 'Classic', 'Country', 'Disco', 'Hiphop', 'Jazz', 'Metal', 'Pop', 'Reggae', 'Rock'}

            # genres_set.remove(track_genres)


            # df_genres = pd.get_dummies(df_all['genres'])

            # df_genres.drop(genres_set,axis=1,inplace=True)

            
            # df_all = pd.concat([df_all,df_genres],axis=1)

            
            

            df_all_drop = df_all.drop(['name','artist','genres','popularity'],axis=1)
## Z-Score
            df_all_drop = (df_all_drop - df_all_drop.mean())/df_all_drop.std()

            # df_all_drop[track_genres] = df_all_drop[track_genres] / 5
            
            selected_track = df_all_drop.loc[track_id,:]

            
            
## Euclidian Distance
            df_all_drop['euclidean_distance'] = df_all_drop.apply(euclidean_distance,selected_track_data=selected_track,axis=1)
            
            df_all['euclidean_distance'] = 0

            
            df_all.update(df_all_drop)
            
            df_sorted = df_all.sort_values(by='euclidean_distance')

            df_sorted = df_sorted.drop(track_id)

            


## Top K 
            similar_tracks = df_sorted.head(k)
            similar_tracks = similar_tracks.reset_index()
            data_dict = similar_tracks.to_dict(orient='records')
            
                
            serializer = self.get_serializer(data=data_dict, many=True)

            if serializer.is_valid():
                # elapsed_time = time.time()- start_time
                # print(elapsed_time)
                return Response(serializer.data) 

        
        except Exception as e:
            return Response({'error': str(e)}, status=500)           
            
            

#### Şarkıya verilen puanı alma yaratma ##
class TrackUserModelCreateView(generics.CreateAPIView):
    
    serializer_class = TrackUserModelSerializer

    def create(self, request, *args, **kwargs):
        start_time = time.time()
        user = request.user
        
        track = request.data.get('Track') 
        

        last_data = request.data.copy()
        
        last_data['User'] = user.id
        
        
        exist = TrackUserModel.objects.filter(User=user, Track=track).first()
        
        if exist:
            if 'rating' in request.data and request.data['rating'] == 0:
                
                exist.delete()
                return Response({'message': 'Mevcut kayıt silindi.'}, status=status.HTTP_200_OK)
            
            serializer = self.get_serializer(exist, data={'rating': request.data['rating']}, partial=True)
            
        else:
            
            serializer = self.get_serializer(data=last_data)
            
            
        
        serializer.is_valid(raise_exception=True)
        
        

        
        serializer.validated_data['User'] = user
        serializer.save(User=user)
        
        elapsed_time = time.time() - start_time
        print(elapsed_time)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class TreeDistanceReccommend(generics.ListAPIView):
    serializer_class = SimilarTrackSerializer
    queryset = Track.objects.all()
    

    def list(self, request, *args, **kwargs):
        try:
            starttime =time.time()
            q = self.get_queryset()

            selected = self.kwargs.get('track_id')
            
            df = pd.DataFrame(q.values())
            df.set_index('id',inplace=True)



            att_names_form = 'mfcc{}_{}'

            att_name = []

            for att_type in ['mean', 'median', 'std']:
                att_name.extend([att_names_form.format(att_type, i) for i in range(13)])

            att_spotify =  ['energy', 'danceability', 'loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
            att_name.extend(att_spotify)
            
    
            
            
            attributes = df[att_name]
            
            # attributes = (attributes - attributes.mean())/attributes.std()
            
            genres = df['genres']

            #Verileri ayırma
            at_train,at_test,genres_train,genres_test = train_test_split(attributes,genres)
            
            accur = []
            accur_rf = []
            accur_svm = []

            for i in range(40,49):
            
                features = attributes.columns[:i]
                

                ## modeller
                decision_tree = DecisionTreeClassifier()
                random_forest = RandomForestClassifier(n_estimators=50)
                svm = SVC(kernel='linear')
                
                decision_tree.fit(at_train[features],genres_train)
                random_forest.fit(at_train[features], genres_train)
                svm.fit(at_train[features], genres_train)


                genres_predict_rt = random_forest.predict(at_test[features])
                genres_predict_svm = svm.predict(at_test[features])
                genres_predict = decision_tree.predict(at_test[features])

                accur_svm.append(accuracy_score(genres_test,genres_predict_svm))
                accur_rf.append(accuracy_score(genres_test,genres_predict_rt)) 
                accur.append(accuracy_score(genres_test,genres_predict))
                
            
            # print(accur)
            # print(accur_rf)
            # print(accur_svm)

            # print(sum(accur)/len(accur))
            # print(sum(accur_rf)/len(accur_rf))
            # print(sum(accur_svm)/len(accur_svm))


            all_accur = accur + accur_rf + accur_svm

            ac = max(all_accur)
            # ac = max(accur)
            
            ac_max_index = (all_accur.index(ac) % 9) + 40
            # print(ac_max_index)
            drop_att = att_name[ac_max_index:]
            # print(drop_att)

            # max_ac_index= accur.index(ac) + 40
            # drop_att = att_name[max_ac_index:]
            

            
            df_drop=df.drop(drop_att,axis=1)
            
            df_drop.drop(['name','artist','genres','popularity'],inplace=True,axis=1)
            ##Euclidian devamı
            df_drop = (df_drop - df_drop.mean())/df_drop.std()
            
            selected_df = df_drop.loc[selected,:]
            
            df_drop['euclidean_distance'] = df_drop.apply(euclidean_distance,selected_track_data=selected_df,axis=1)
            
            df['euclidean_distance'] = 0

            df.update(df_drop)

            df_sorted = df.sort_values(by='euclidean_distance')
            df_sorted = df_sorted.drop(selected)

            similar_tracks = df_sorted.head(20)
            
            
            similar_tracks = similar_tracks.reset_index()
            
            data_dict = similar_tracks.to_dict(orient='records')
            
            serializer = self.get_serializer(data=data_dict, many=True)

            if serializer.is_valid():
                
                elapsed_time = time.time()-starttime
                print(elapsed_time)
                return Response(serializer.data)
             
        except Exception as e:
            return Response({'error': str(e)}, status=500)


        
class RateList(generics.ListAPIView):
    serializer_class = RateSerializer
    
    def get_queryset(self):
        
        user = self.request.user
        track_id = self.kwargs.get('track_id', None)
        
        track_user = TrackUserModel.objects.filter(Track_id=track_id, User=user)

        return track_user
    
    def list(self, request, *args, **kwargs):
        # start_time = time.time()
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            # elapsed_time = time.time()- start_time
            # print(elapsed_time)
            return Response(serializer.data)
        else:
            return Response({'error': 'Kayıt bulunamadı'}, status=status.HTTP_404_NOT_FOUND)




class UserTrackList(generics.ListAPIView):
    serializer_class = UserTrackListSerializer

    def get_queryset(self):
        user_query = self.request.user
        user_tracks = TrackUserModel.objects.filter(User=user_query)
        
        return user_tracks
    def list(self, request, *args, **kwargs):
        
        start_time = time.time()

        response = super().list(request, *args, **kwargs)

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        return response
    


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


           




class UserLoginView(APIView):
    serializer_class= UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Hatali Giris'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        request.auth.delete()

        return Response({'message': 'Cikis Basarili'}, status=status.HTTP_200_OK)