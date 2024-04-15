from tracks.api.views import SimilarTrackListView, TrackListView,ListTrackByGenres,ListTrackByArtist,ListSimilarUserReccom,TrackUserModelCreateView, UserTrackList, LogoutUserView,UserRegistrationView,UserLoginView,TreeDistanceReccommend,RateList

from django.urls import path

urlpatterns = [
        path('similar_tracks/<str:track_id>/<int:k>', SimilarTrackListView.as_view()),
        path('tracks/',TrackListView.as_view()),                    
        path('track_by_genres/<str:genres>/',ListTrackByGenres.as_view()),
        path('track_by_artist/<str:artist>/', ListTrackByArtist.as_view()),
        path('list_user_user_reccom/', ListSimilarUserReccom.as_view()),
        path('register/', UserRegistrationView.as_view()),
        path('login/', UserLoginView.as_view()),
        path('logout/', LogoutUserView.as_view()),
        path('usertrack/',TrackUserModelCreateView.as_view()),
        path('userrating/', UserTrackList.as_view()),
        path('treedistancereccom/<str:track_id>/', TreeDistanceReccommend.as_view()),
        path('rating/<str:track_id>/', RateList.as_view()),
]