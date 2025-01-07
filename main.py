import os
from mutagen import File
from mutagen.mp3 import MP3
from pathlib import Path

MUSIC_DIR = "/Users/drewmilbrath/Music/Music/Media.localized"

def check_artwork(file_path):
    try:
        audio = File(file_path)
        
        # Handle MP3 files
        if file_path.endswith('.mp3'):
            if not audio.tags or not audio.tags.getall('APIC'):
                return True  # Missing artwork
                
        # WAV files don't typically support embedded artwork
        elif file_path.endswith('.wav'):
            return True  # Consider all WAV files as missing artwork
            
        return False  # Has artwork
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def main():
    missing_artwork = []
    
    # Walk through the music directory
    for root, dirs, files in os.walk(MUSIC_DIR):
        for file in files:
            if file.endswith(('.mp3', '.wav')):
                file_path = os.path.join(root, file)
                if check_artwork(file_path):
                    missing_artwork.append(file_path)
    
    # Sort the results alphabetically by filename
    missing_artwork.sort(key=lambda x: os.path.basename(x).lower())
    
    # Print sorted results
    print("\nFiles missing artwork:")
    for file in missing_artwork:
        print(f"- {os.path.basename(file)}")
    print(f"\nTotal files missing artwork: {len(missing_artwork)}")

if __name__ == "__main__":
    main()
