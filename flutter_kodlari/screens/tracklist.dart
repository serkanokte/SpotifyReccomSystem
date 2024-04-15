import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:flutter_musicsystem/screens/trackdetail.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_musicsystem/models/tracks.dart';
import 'package:provider/provider.dart';

// şarkıların listelendiği sayfa
class TrackListScreen extends StatelessWidget {
  final String apiUrl;

  const TrackListScreen(this.apiUrl, {super.key});

  Future<List<Track>> fetchTrack(String? token) async {
    
    final response = await http.get(
      Uri.parse(apiUrl),
      headers: {'Authorization': token!}, 
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      List<Track> tracks = data.map((track) => Track.fromJson(track)).toList();
      
      return tracks;
    } 
    else{ 
      Map<String, dynamic> errorData = json.decode(response.body);
      
      if (errorData['error'] == 'Yetersiz degerlendirme sayisi.'){

          throw Exception('En Az 10 şarkı değerlendirmeniz gerekli');
      }


      else {
        throw Exception('En Az 1 şarkıya 4 üstü puan vermeniz gerekli');
          
       }
      }
    }
  
  @override
  Widget build(BuildContext context) {
     final authProvider =Provider.of<AuthProvider>(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Şarkı Listesi'),
      ),
      body: FutureBuilder<List<Track>>(
        future: fetchTrack(authProvider.token),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text(
            '${snapshot.error.toString().split(":").length > 1 ? snapshot.error.toString().split(":")[1].trim() : snapshot.error}',
                    style: const TextStyle(
            fontWeight: FontWeight.bold, 
            fontSize: 18.0, 
          ),
            )
            );
          } else {
            List<Track> tracks = snapshot.data!;
            return ListView.builder(
              itemCount: tracks.length,
              itemBuilder: (context, index) {
                return GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => TrackDetailScreen(tracks[index]),
                      ),
                    );
                  },
                  child: ListTile(
                    title: Text(tracks[index].name),
                    subtitle: Text('${tracks[index].artist} - ${tracks[index].genres}'),
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}

