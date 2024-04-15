
import 'package:flutter/material.dart';

import 'package:flutter_musicsystem/screens/tracklist.dart';


// şarkı türlerinin listelendiği sayfa//

class GenresScreen extends StatelessWidget {
  final List<String> buttonTexts = ['Rock', 'Pop', 'HipHop', 'Jazz', 'Classic', 'Country', 'Blues', 'Metal', 'Reggae', 'Disco'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tür Seçin'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2, 
            crossAxisSpacing: 8.0, 
            mainAxisSpacing: 8.0, 
          ),
          itemCount: 10,
          itemBuilder: (context, index) {
           return ElevatedButton(
              onPressed: () {
                onButtonPressed(context, buttonTexts[index]);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: index % 2 == 1 ? Colors.red : Colors.blue, 
                padding: const EdgeInsets.all(16.0), 
              ),
              child: Text(
                buttonTexts[index],
                style: const TextStyle(fontSize: 16),
              ),
            );
          },
        ),
      ),
    );
  }
  void onButtonPressed(BuildContext context, String genre) {
    
    String apiUrl = 'http://10.0.2.2:8000/api/track_by_genres/$genre';
    
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => TrackListScreen(apiUrl),
      ),
    );
  }
    

}


