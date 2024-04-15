import 'package:flutter/material.dart';
import 'package:flutter_musicsystem/screens/pagemain.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_musicsystem/provider/tokenprovider.dart';
import 'package:provider/provider.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  String _username = '';
  String _password = '';
  String _confirmPassword = '';

  Future<void> _makeApiRequest() async {
    const apiUrl = 'http://10.0.2.2:8000/api/register/';
    if (_password != _confirmPassword) {
      _showErrorSnackBar('Şifreler Eşleşmiyor');

      return;
    }

    
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': _username,
        'password': _password,
        'password_confirmation': _confirmPassword,
      }),
    );
    
    if (response.statusCode == 201) {
      
      final Map<String, dynamic> responseData = jsonDecode(response.body);

      String token = responseData['token'];
      token = "Token $token";

      Provider.of<AuthProvider>(context, listen: false).setToken(token);
      Provider.of<AuthProvider>(context, listen: false).setUsername(_username);

      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const PageMain()),
        (route) => false,
      );
      
    } else {
      Map<String, dynamic> errorResponse = jsonDecode(response.body);
      if(errorResponse.containsKey('username') &&
        errorResponse['username'][0] == 'A user with that username already exists.'){
         
        _showErrorSnackBar('Bu Kullanıcı adı alınmıştır');
      }
      
      else{_showErrorSnackBar('Şifre En az 8 harfli olmalıdır');
          }
      
         
    }
  }
   void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Kayıt Olma Ekranı'),
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
                  _username = value!;
                },
                decoration: const InputDecoration(
                  labelText: 'Kullanıcı Adı',
                ),
              ),
              const SizedBox(height: 16.0),
              TextFormField(
                onSaved: (value) {
                  _password = value!;
                },
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Şifre',
                ),
              ),
              const SizedBox(height: 16.0),
              TextFormField(
                onSaved: (value) {
                  _confirmPassword = value!;
                },
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Şifre Tekrarı',
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
                child: const Text('Kayıt Ol'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}