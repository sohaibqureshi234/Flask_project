import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io' show Platform;
import '../models/task_model.dart';

class ApiService {
  String? _token;

  // Determine the base URL based on the platform
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:5001';
    } else {
      return 'http://127.0.0.1:5001';
    }
  }

  static const String taskEndpoint = '/tasks';

  // Helper for headers
  Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    if (_token != null) 'Authorization': 'Bearer $_token',
  };

  // AUTH: Login
  Future<void> login(String username, String password) async {
    final url = '$baseUrl/login';
    print('Calling LOGIN: $url');
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'username': username, 'password': password}),
      );
      print('Response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _token = data['access_token'];
      } else {
        final error = json.decode(response.body)['error'] ?? 'Login failed';
        throw Exception(error);
      }
    } catch (e) {
      print('Auth Error: $e');
      rethrow;
    }
  }

  // AUTH: Register
  Future<void> register(String username, String password) async {
    final url = '$baseUrl/register';
    print('Calling REGISTER: $url');
    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'username': username, 'password': password}),
    );
    print('Response status: ${response.statusCode}');

    if (response.statusCode != 201) {
      final error =
          json.decode(response.body)['error'] ?? 'Registration failed';
      throw Exception(error);
    }
  }

  // GET all tasks
  Future<List<Task>> getTasks() async {
    final url = '$baseUrl$taskEndpoint';
    print('Calling GET: $url');
    final response = await http.get(Uri.parse(url), headers: _headers);
    print('Response status: ${response.statusCode}');

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Task.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load tasks (${response.statusCode})');
    }
  }

  // POST a new task
  Future<void> addTask(String name) async {
    final url = '$baseUrl$taskEndpoint';
    print('Calling POST: $url');
    final response = await http.post(
      Uri.parse(url),
      headers: _headers,
      body: json.encode({'name': name}),
    );
    print('Response status: ${response.statusCode}');

    if (response.statusCode != 201) {
      throw Exception('Failed to add task');
    }
  }

  // PUT / update a task
  Future<void> updateTask(String oldName, String newName) async {
    final url = '$baseUrl$taskEndpoint/$oldName';
    print('Calling PUT: $url');
    final response = await http.put(
      Uri.parse(url),
      headers: _headers,
      body: json.encode({'name': newName}),
    );
    print('Response status: ${response.statusCode}');

    if (response.statusCode != 200) {
      throw Exception('Failed to update task');
    }
  }

  // DELETE a task
  Future<void> deleteTask(String name) async {
    final url = '$baseUrl$taskEndpoint/$name';
    print('Calling DELETE: $url');
    final response = await http.delete(Uri.parse(url), headers: _headers);
    print('Response status: ${response.statusCode}');

    if (response.statusCode != 200) {
      throw Exception('Failed to delete task');
    }
  }

  bool get isAuthenticated => _token != null;
  void logout() => _token = null;
}
