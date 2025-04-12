# Automated-Video-Editor

A Machine Learning-based project designed to detect cheering moments in audio and video files using a Random Forest classifier. This repository processes audio to identify cheering segments, visualizes predictions on waveforms, and creates highlight reels from video inputs by extracting exciting moments. Ideal for applications in sports analysis, event summarization, or interactive media.

## Features
- **Audio Classification**: Uses Librosa to extract features (MFCC, spectral centroid, zero-crossing rate) and a Random Forest model to classify audio segments as "Cheer" or "No Cheer."
- **Waveform Visualization**: Plots audio waveforms with color-coded predictions (green for cheer, red for no cheer) using Matplotlib.
- **Video Highlight Generation**: Processes videos to extract cheering moments, merges segments, and creates a highlight reel using MoviePy.
- **Segment-Based Analysis**: Analyzes audio in 1-second (audio) or 2-second (video) segments for precise detection.
- **Model Persistence**: Saves and loads trained models with Pickle for reusability.

## Tech Stack
- **Languages**: Python
- **Libraries**: 
  - Scikit-learn (Random Forest Classifier)
  - Librosa (Audio feature extraction)
  - MoviePy (Video processing)
  - Matplotlib (Visualization)
  - NumPy (Numerical operations)
- **Tools**: FFmpeg (Audio extraction), Jupyter Notebook (Development)
- **Environment**: Google Colab-compatible

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BigBeanTheory/Automated-Video-Editor.git
   cd Automated-Video-Editor
