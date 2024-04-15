import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/screens/pagemain.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:provider/provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  String _textField1Value = '';
  String _textField2Value = '';

  Future<void> _makeApiRequest() async {
    const apiUrl = 'http://10.0.2.2:8000/api/login/';
    
  
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': _textField1Value,
        'password': _textField2Value,
      }),
    );

    if (response.statusCode == 200) {
      
      final Map<String, dynamic> responseData = jsonDecode(response.body);
      
      String token = responseData['token'];
      token = "Token $token";

      Provider.of<AuthProvider>(context, listen: false).setToken(token);
      Provider.of<AuthProvider>(context, listen: false).setUsername(_textField1Value);

      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (context) => const PageMain()),(route) => false,);
      
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("Kullanıcı Adı veya Şifre yanlış"),
        duration: Duration(seconds: 2),
      ),
    );

    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Giriş Ekranı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                onSaved: (value) {
                  _textField1Value = value!;
                },
                decoration: const InputDecoration(
                  labelText: 'Kullanıcı Adı',
                ),
              ),
              const SizedBox(height: 16.0),
              TextFormField(
                onSaved: (value) {
                  _textField2Value = value!;
                },
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Şifre',
                ),
              ),
              const SizedBox(height: 24.0),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                      _formKey.currentState!.save();
                      _makeApiRequest();
                  }
                },
                child: const Text('Giriş Yap'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}