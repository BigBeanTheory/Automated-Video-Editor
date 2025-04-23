const express = require('express');
const multer = require('multer');
const { execFile } = require('child_process');
const path = require('path');
const app = express();

const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('video'), (req, res) => {
  const inputPath = req.file.path;
  const outputPath = 'public/highlight_reel.mp4';

  // Run the video processing executable
  execFile('process_video.exe', [inputPath, outputPath], (err) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Error processing video');
    }

    // Return the URL of the processed video
    res.send(`http://your-server-url/highlight_reel.mp4`);
  });
});

app.use(express.static('public')); // Serve processed video

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
