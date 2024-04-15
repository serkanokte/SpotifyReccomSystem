import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/models/tracks.dart';
import 'package:flutter_musicsystem/screens/trackdistancelist.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:provider/provider.dart';

class TrackDetailScreen extends StatefulWidget {
  final Track track;
  
  const TrackDetailScreen(this.track, {super.key});

  @override
  _TrackDetailScreenState createState() => _TrackDetailScreenState();
}

class _TrackDetailScreenState extends State<TrackDetailScreen> {
  double initialRating = 0;

  @override
  void initState() {
    super.initState();
    fetchRating();
  }

  Future<void> fetchRating() async {
     final authProvider = Provider.of<AuthProvider>(context, listen: false); 
     final token = authProvider.token;
    
    final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/rating/${widget.track.id}/'),
    headers: {
        'Authorization': '$token',
        'Content-Type': 'application/json',
      },
    
    );

    


    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      setState(() {
        initialRating = data['rating']; 
      });
    } else {
      initialRating = 0;
    }
  }

  Future<void> updateRating(double newRating) async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final token = authProvider.token;

    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/usertrack/'),
      headers: {
        'Authorization': '$token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'Track': widget.track.id,
        'rating': newRating,
      }),
    );
    if (response.statusCode == 201) {
       ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Rating başarıyla güncellendi'),
          duration: Duration(seconds: 2), 
        ),
      );
    } 
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Şarkı Detayı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Şarkı Adı: ${widget.track.name}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              'Şarkıcı: ${widget.track.artist}',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 8),
            Text(
              'Şarkı Türü: ${widget.track.genres}',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Text(
                  'Rating: ',
                  style: TextStyle(fontSize: 18),
                ),
                RatingBar.builder(
                  initialRating: initialRating,
                  minRating: 0,
                  direction: Axis.horizontal,
                  allowHalfRating: true,
                  itemCount: 5,
                  itemPadding: const EdgeInsets.symmetric(horizontal: 4.0),
                  itemBuilder: (context, _) => const Icon(
                    Icons.star,
                    color: Colors.amber,
                  ),
                  onRatingUpdate: (rating) {
                    updateRating(rating);
                  },
                ),
              ],
            ),
            const SizedBox(height: 16), 
           Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  ElevatedButton(
                    onPressed: () {
                      String apiUrl = 'http://10.0.2.2:8000/api/similar_tracks/${widget.track.id}/50';
                       Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => TrackDistanceListScreen(apiUrl),
                        ),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.yellow,
                    ),
                    child: const Padding(
                      padding: EdgeInsets.all(16.0),
                      child: Text(
                        'Benzer Şarkı Bul',
                        style: TextStyle(fontSize: 20),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  ElevatedButton(
                    onPressed: () {
                      String apiUrl = 'http://10.0.2.2:8000/api/treedistancereccom/${widget.track.id}';
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => TrackDistanceListScreen(apiUrl),
                        ),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                    ),
                    child: const Padding(
                      padding: EdgeInsets.all(16.0),
                      child: Text(
                        'Sınıflandırma Algoritmalarına Göre Öneri Bul',
                        style: TextStyle(fontSize: 20),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}