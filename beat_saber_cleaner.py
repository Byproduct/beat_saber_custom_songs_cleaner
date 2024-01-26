# Run this script from the root of your Beat Saber folder.

# It will delete any custom songs that are not included in any custom playlist. 
# (These are probably forgotten about and just taking up space.)
# Made for Windows 10 / Steam version of Beat Saber.


import os
import re
import shutil
import sys

playlist_directory = "Playlists"
custom_songs_directory = "Beat Saber_Data\CustomLevels"

root_path = os.path.dirname(os.path.abspath(__file__))
playlist_directory = os.path.join(root_path, playlist_directory)
custom_songs_directory = os.path.join(root_path, custom_songs_directory)


os.system('cls')

if not os.path.isdir(playlist_directory) or not os.path.isdir(custom_songs_directory):
    print("Failed to find directories.")
    print("This script should be run from the root of your Beat Saber folder in Windows.")
    sys.exit(1)
    
print("This script will delete any Beat Saber custom song files that are not included in any of your custom playlists.")
print("\nMade for Windows 10/11.")
print("\nPlaylist entries that don't include keys (older format?) will not get detected. Any such unintentionally deleted songs can be easily re-downloaded in-game though.")
print("\nMake sure you have a backup of Beat_Saber_Data/CustomLevels before proceeding!")
print("\nEnter to proceed, ctrl+c to cancel.")

try:
    input()
except KeyboardInterrupt:
    print("\nCancelled.")
    sys.exit(1)


def get_directory_size(path):
    total_size = 0
    file_count = 0

    for root_path, dirs, files in os.walk(path):
        file_count += len(files)
        for file in files:
            file_path = os.path.join(root_path, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)

    total_size = round(total_size / (1024**2))  # return megabytes
    return file_count, total_size

def extract_keys_from_playlists(directory):
    # Will also extract song names, although these are not used at the moment
    key_pattern = r'"key": "(\w{3,5})"'
    name_pattern = r'"songName": "(.*?)"'
    keys = []
    names = []
    for filename in os.listdir(directory):
        if filename.endswith(".bplist"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                keys.extend(re.findall(key_pattern, content))
                names.extend(re.findall(name_pattern, content))
    
    return keys

def check_directories(keys,custom_songs_directory):
    all_song_directories = {key.lower(): False for key in keys}
    directories_without_keys = []

    for directory_name in os.listdir(custom_songs_directory):
        directory_key = directory_name.split(" ")[0].lower()
        if directory_key in all_song_directories:
            all_song_directories[directory_key] = True
        else:
            directories_without_keys.append(directory_name)

    return directories_without_keys

# Directory size before operation
file_count_pre, total_size_pre = get_directory_size(custom_songs_directory)

# Extract keys and song names from playlists
extracted_keys = extract_keys_from_playlists(playlist_directory)
directories_without_keys = check_directories(extracted_keys, custom_songs_directory)

if not directories_without_keys:
    print("\n\n...Could not find any songs to delete ¯\\_(._.)_/¯")
    sys.exit(1)

# Delete orphaned custom songs
for path in directories_without_keys:
    song_directory = os.path.join(root_path, custom_songs_directory, path)
    _, directory_size = get_directory_size(song_directory)
    try:
        shutil.rmtree(song_directory)
        print(f"Deleted {directory_size: >4} MB: {path}")
    except:
        print(f"Could not delete {song_directory}")
        
# Directory size after operation
file_count_post, total_size_post = get_directory_size(custom_songs_directory)
file_count_saved = file_count_pre - file_count_post
total_size_saved = total_size_pre - total_size_post

print(f"\nBefore deleting: {file_count_pre} files, {total_size_pre} MB.")
print(f"After deleting:  {file_count_post} files, {total_size_post} MB.")
print(f"Space freed:     {file_count_saved} files, {total_size_saved} MB.")