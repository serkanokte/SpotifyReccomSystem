import 'dart:convert';
import 'package:flutter_musicsystem/models/tracks.dart';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:flutter_musicsystem/screens/trackdetail.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';


class UserRateScreen extends StatefulWidget {
  const UserRateScreen({super.key});

  @override
  _UserRateScreenState createState() => _UserRateScreenState();
}

class _UserRateScreenState extends State<UserRateScreen> {
  List<Map<String, dynamic>> trackList = [];
   late AuthProvider authprov;


  @override
  void initState() {
    super.initState();
    authprov = Provider.of<AuthProvider>(context, listen: false);
    fetchData();
  }

  Future<void> fetchData() async {
    final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/userrating/'),headers: {'Authorization': authprov.token!});

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      setState(() {
        trackList = List<Map<String, dynamic>>.from(data);
      });
    } else {
      throw Exception('veri çekilemedi: ${response.statusCode}');
    }
  }

  Future<void> updateRating(double newRating,Map<String, dynamic> track) async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final token = authProvider.token;

    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/usertrack/'),
      headers: {
        'Authorization': '$token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'Track': track['id'],
        'rating': newRating,
        
      }),
    );
    if (response.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("Puan Bilgisi başarılı bir şekilde alındı"),
        duration: Duration(seconds: 1),
      ),
    );
    } 
  }
  

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: const Text('Şarkı Listesi'),
      ),
      body: ListView.builder(
        itemCount: trackList.length,
        itemBuilder: (context, index) {
          final trackUserModel = trackList[index];
          final track = trackUserModel['track'];
          
          return ListTile(
            title: Text(track['name']),
            subtitle: Text('${track['artist']} - ${track['genres']}'),
            trailing: RatingBar.builder(
              initialRating: trackUserModel['rating'],
              minRating: 0,
              direction: Axis.horizontal,
              allowHalfRating: true,
              itemCount: 5,
              itemSize: 20,
              itemPadding: const EdgeInsets.symmetric(horizontal: 2.0),
              itemBuilder: (context, _) => const Icon(
                Icons.star,
                color: Colors.amber,
              ),
              onRatingUpdate: (rating) {
                updateRating(rating, track);
              },
            ),
            onTap: (){
                    Track trackObject = Track(
                      id: track['id'],
                      name: track['name'],
                      artist: track['artist'],
                      genres: track['genres'],
                    );
               Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => TrackDetailScreen(trackObject), )
                        );
            }
          );
        },
      ),
    );
  }
}