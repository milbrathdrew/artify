import os
from mutagen import File
from mutagen.mp3 import MP3
from pathlib import Path
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='music_artwork_check.log'
)

MUSIC_DIR = "/Users/drewmilbrath/Music/Music/Media.localized"

def check_artwork(file_path):
    try:
        audio = File(file_path)
        
        # Handle MP3 files
        if file_path.endswith('.mp3'):
            if not audio or not audio.tags or not audio.tags.getall('APIC'):
                return True  # Missing artwork
                
        # WAV files don't typically support embedded artwork
        elif file_path.endswith('.wav'):
            return True  # Consider all WAV files as missing artwork
            
        return False  # Has artwork
        
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return None

def count_music_files(directory):
    """Count total number of music files for progress bar"""
    return sum(1 for root, _, files in os.walk(directory) 
              for file in files if file.endswith(('.mp3', '.wav')))

def main():
    missing_artwork = []
    error_files = []
    
    # Get total file count for progress bar
    total_files = count_music_files(MUSIC_DIR)
    
    # Walk through the music directory with progress bar
    with tqdm(total=total_files, desc="Scanning files") as pbar:
        for root, dirs, files in os.walk(MUSIC_DIR):
            for file in files:
                if file.endswith(('.mp3', '.wav')):
                    file_path = os.path.join(root, file)
                    result = check_artwork(file_path)
                    
                    if result is True:  # Missing artwork
                        missing_artwork.append(file_path)
                    elif result is None:  # Error occurred
                        error_files.append(file_path)
                        
                    pbar.update(1)
    
    # Sort the results alphabetically by filename
    missing_artwork.sort(key=lambda x: os.path.basename(x).lower())
    
    # Print results
    print("\nFiles missing artwork:")
    for file in missing_artwork:
        print(f"- {os.path.basename(file)}")
    
    print(f"\nTotal files missing artwork: {len(missing_artwork)}")
    
    if error_files:
        print("\nFiles with errors:")
        for file in error_files:
            print(f"- {os.path.basename(file)}")
        print(f"\nTotal files with errors: {len(error_files)}")
        print("\nCheck music_artwork_check.log for detailed error information")

if __name__ == "__main__":
    main()
