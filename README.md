# 🎙️ Subtitle Generator (Speech Recognition) using Whisper

![Alt Text](assets/img_seg_thumbnail.png)

## 🔎 About
This project focuses english speech reconition and transform it into subtitles (.srt) using the Whisper (medium.en) model.

Project languages:
* en
  
## 📦 Dependencies
|  Name  |  Version  |
|--------|-----------|
|[streamlit](https://pypi.org/project/streamlit/)|1.34.2|
|[srt](https://pypi.org/project/srt/)|3.5.3|
|[whisper](https://pypi.org/project/whisper/)|1.1.10|


## 🖥️ Requirements
* Operating System (OS): Windows 10, Mac, Linux.
* `python==3.9.9` and `pytorch==1.10.1`
* Integrated Development Environment (IDE): VSCode.
* Web Browser: Google Chrome, Microsoft Edge, Firefox, Safari.

## ⬇️ Installation
### Make a directory
```
mkdir img_segmentation_app
```
```
cd img_segmentation_app
```
### Create and activate environment
```
python -m venv venv
```
```
venv\Scripts\activate 
```
### Install dependencies
```
pip install openai-whisper streamlit srt ffmpeg
```

setup FFmpeg:
1. Download and extract FFmpeg: https://ffmpeg.org/download.html
2. Create new terminal
3. run:
   ```
   $env:PATH = "C:\ffmpeg\bin;" + $env:PATH
   ```
4. activate venv again:
   ```
   venv\Scripts\activate 
   ```
   
### Run App.
```
streamlit run app.py
```

## 🥼 Author(s) / Contributor(s)
* Wicaksono Hanif Supriyanto

## 📚 References
* Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). Robust speech recognition via large-scale weak supervision. arXiv. https://arxiv.org/abs/2212.04356
* Inspired by [Bikin Subtitle Otomatis dengan Python (Python Tutorial)](https://www.youtube.com/watch?v=ny-INGzkbrs&list=LL&index=5&t=285s) by ngodein.
