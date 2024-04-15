import 'package:flutter/material.dart';

class AuthProvider with ChangeNotifier {
  String? _token;
  String? _username;

  String? get token => _token;
  String? get username => _username;


  setToken(String token) {
    _token = token;
    notifyListeners();
  }
  setUsername(String username) {
    _username = username;
    notifyListeners();
  }

}