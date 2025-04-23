import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:video_player/video_player.dart';

class VideoUploadPage extends StatefulWidget {
  @override
  _VideoUploadPageState createState() => _VideoUploadPageState();
}

class _VideoUploadPageState extends State<VideoUploadPage> {
  VideoPlayerController? _controller;
  String? _videoUrl;

  // Pick a video from gallery
  Future<void> _pickVideo() async {
    final ImagePicker _picker = ImagePicker();
    final XFile? video = await _picker.pickVideo(source: ImageSource.gallery);
    
    if (video != null) {
      _uploadVideo(File(video.path));
    }
  }

  // Upload video to backend
  Future<void> _uploadVideo(File videoFile) async {
    final uri = Uri.parse('http://your-backend-server/upload');
    var request = http.MultipartRequest('POST', uri);

    request.files.add(await http.MultipartFile.fromPath('video', videoFile.path));
    var response = await request.send();

    if (response.statusCode == 200) {
      final result = await response.stream.bytesToString();
      setState(() {
        _videoUrl = result; // Expecting the URL of the processed video
      });

      _playProcessedVideo();
    } else {
      print('Failed to upload video');
    }
  }

  // Play the processed video
  void _playProcessedVideo() {
    if (_videoUrl != null) {
      _controller = VideoPlayerController.network(_videoUrl!)
        ..initialize().then((_) {
          setState(() {});
          _controller?.play();
        });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Video Upload & Play")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickVideo,
              child: Text("Pick Video"),
            ),
            if (_controller != null && _controller!.value.isInitialized)
              Container(
                height: 200,
                child: VideoPlayer(_controller!),
              ),
            if (_videoUrl != null) Text('Processed video is ready!'),
          ],
        ),
      ),
    );
  }
}
