
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/models/tracks.dart';
import 'package:flutter_musicsystem/screens/trackdetail.dart';
import 'package:http/http.dart' as http;


class TrackFilterScreen extends StatefulWidget {
  const TrackFilterScreen({super.key});

  @override
  _TrackFilterScreenState createState() => _TrackFilterScreenState();
}

class _TrackFilterScreenState extends State<TrackFilterScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Track> allTracks = [];
  List<Track> filteredTracks = [];

  @override
  void initState() {
    super.initState();
    fetchTracks();
  }

  Future<void> fetchTracks() async {
    var response = await http.get(Uri.parse('http://10.0.2.2:8000/api/tracks'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      List<Track> tracks = data.map((track) => Track.fromJson(track)).toList();

      setState(() {
        allTracks = tracks;
        filteredTracks = allTracks;
      });
    } else {
      throw Exception('API erişimi başarısız');
    }
  }

  void filterTracks(String query) {
    List<Track> filteredList = [];
    for (var track in allTracks) {
      if (track.name.toLowerCase().contains(query.toLowerCase())||
          track.artist.toLowerCase().contains(query.toLowerCase())) {
        filteredList.add(track);
      }
    }
    setState(() {
      filteredTracks = filteredList;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Şarkı Listesi'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _searchController,
              decoration: const InputDecoration(
                labelText: 'Şarkı Ara',
                hintText: 'Şarkıcı ya da şarkı adı girin',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(10.0)),
                ),
              ),
              onChanged: (value) {
                filterTracks(value);
              },
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: filteredTracks.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(filteredTracks[index].name),
                    subtitle: Text('${filteredTracks[index].artist},${filteredTracks[index].genres}'),
                    onTap: (){Navigator.push(
                         context,
                    MaterialPageRoute(
                      builder: (context) => TrackDetailScreen(filteredTracks[index]),
                    ),
                  );
                    } 
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}