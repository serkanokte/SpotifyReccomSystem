import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/models/tracks.dart';
import 'package:flutter_musicsystem/screens/trackdetail.dart';
import 'package:http/http.dart' as http;

// Euclidian distance sonucu olan  şarkıların gösterilmesi

class TrackDistanceListScreen extends StatefulWidget {
  final String apiUrl;

  const TrackDistanceListScreen(this.apiUrl, {super.key});

  @override
  _TrackDistanceListScreenState createState() => _TrackDistanceListScreenState();
}

class _TrackDistanceListScreenState extends State<TrackDistanceListScreen> {
  int selectedItemCount = 20; 

  Future<List<Track>> fetchTrackEuclidean() async {
    try {
      final response = await http.get(Uri.parse(widget.apiUrl));

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        
        List<Track> tracks = data.map((track) => Track.fromJson(track)).toList();
        return tracks.take(selectedItemCount).toList();
      } else {
        throw Exception('Şarkı bulunamadı');
      }
    } catch (error) {
      throw Exception('API bağlantısı başarısız $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mesafe Listesi'),
        actions: [
        if (!widget.apiUrl.contains('http://10.0.2.2:8000/api/treedistancereccom/'))
          DropdownButton<int>(
            value: selectedItemCount,
            onChanged: (int? newValue) {
              if (newValue != null) {
                setState(() {
                  selectedItemCount = newValue;
                });
              }
            },
            items: [5, 10, 15, 20, 50].map<DropdownMenuItem<int>>((int value) {
              return DropdownMenuItem<int>(
                value: value,
                child: Text('$value'),
              );
            }).toList(),
          ),
        ],
      ),
      body: FutureBuilder<List<Track>>(
        future: fetchTrackEuclidean(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Hata: ${snapshot.error}'),
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
                    subtitle: Text('${tracks[index].genres}, ${tracks[index].euclideanDistance}'),
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
