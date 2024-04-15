import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/main.dart';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:flutter_musicsystem/screens/genres.dart';
import 'package:flutter_musicsystem/screens/rate.dart';
import 'package:flutter_musicsystem/screens/trackfilter.dart';
import 'package:flutter_musicsystem/screens/tracklist.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;

//Kullanıcıların login sonrası Göreceği anasayfa
class PageMain extends StatelessWidget {
  const PageMain({super.key});

  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context, listen: false);  

    return Scaffold(
      appBar: AppBar(
        title: Align(
        alignment: Alignment.centerRight,
        child: Text(authProvider.username ?? "a"),
        ),),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder:(context) => GenresScreen()));
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
              child: const Padding(
                padding: EdgeInsets.all(20.0),
                child: Text('Şarkılar', style: TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context)=> const TrackFilterScreen()));
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              child: const Padding(
                padding: EdgeInsets.all(20.0),
                child: Text('Şarkı-Şarkıcı Ara', style: TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
              String apiUrl = 'http://10.0.2.2:8000/api/list_user_user_reccom/';
              Navigator.push(context,MaterialPageRoute(builder:(context) =>TrackListScreen(apiUrl)));
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
              child: const Padding(
                padding: EdgeInsets.all(20.0),
                child: Text('Değerlendirmeme Göre Şarkı Öner', style: TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(context, MaterialPageRoute(builder: (context) => const UserRateScreen()));
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.yellow),
                  child: const Padding(
                    padding: EdgeInsets.all(20.0),
                    child: Text('Değerlendirmelerim', style: TextStyle(fontSize: 14)),
                  ),
                ),
                ElevatedButton(
                  onPressed: () async{
                    final authProvider = Provider.of<AuthProvider>(context, listen: false);
                    final token = authProvider.token;
                    final response= await http.post(Uri.parse('http://10.0.2.2:8000/api/logout/'),headers: {
                            'Authorization': '$token',
                            'Content-Type': 'application/json',
                      },);
                    if(response.statusCode == 200){

                      
                      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (context) => const FirstPage()), (route) => false);

                    }
                    else{
                      
                    }
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.pink),
                  child: const Padding(
                    padding: EdgeInsets.all(20.0),
                    child: Text('Çıkış Yap', style: TextStyle(fontSize: 14)),
                  ),
                ),
          ],
        ),
          ],
      ),
      ),
    );
  }
}