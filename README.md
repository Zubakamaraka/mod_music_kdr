# Music.kdr Editor

Simple editor for `music.kdr` files from Keep Driving.
![Screenshot_5](https://github.com/user-attachments/assets/028828bb-c371-4c95-936d-f644a27aa589)

[![Download Latest Release](https://img.shields.io/badge/Download-EXE-00FF99?style=for-the-badge&logo=windows)](https://github.com/Zubakamaraka/mod_music_kdr/releases/download/v0.1/music_editor.exe)

## Features
- Edit existing music tracks
- Add new tracks
- English/Russian language toggle

## How to Use
1. Run `music_editor.exe`
2. Click "Browse" to open your music.kdr file
3. View/edit existing tracks
4. Add new tracks using the form:
   - Developer Name
   - Title
   - Artist  
   - Track ID
5. Click "Save" when done

## Requirements
- Python 3.x
- Tkinter

## File Format Example
```kdr
{
    dev_name: Name
    title: Song Title
    artist: Artist
    track: id123
    start: 1
}
