import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/screens/login.dart';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:flutter_musicsystem/screens/register.dart';
import 'package:provider/provider.dart';

//ilk ekran
void main() {
  runApp(ChangeNotifierProvider(
    create: (context) => AuthProvider(),
    child: const MyApp(),
    ),
    );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: FirstPage(),
    );
  }
}

class FirstPage extends StatelessWidget {
  const FirstPage({super.key});
 
  @override
  Widget build(BuildContext context) {
    

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,

          children: [
            
             const Align(
              alignment: Alignment.center,
            child: Text(
                'Müzik Öneri Sistemi',
                style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                
                Navigator.push(context,MaterialPageRoute(builder:(context) => const LoginScreen()));
                
              },
              child: const Text('Giriş Yap'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const RegisterScreen()));
              },
              child: const Text('Kayıt Ol'),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}