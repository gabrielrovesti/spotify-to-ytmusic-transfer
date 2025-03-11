# Spotify to YouTube Music Transfer

A simple script to transfer your playlists from Spotify to YouTube Music.

## Requirements

- Python 3.8 or higher (tested with Python 3.9)
- Spotify account
- YouTube/Google account
- Firefox browser (needed for YouTube Music authentication)

## Quick Instructions

### Windows

1. Download all files to the same folder
2. Double-click on `run-spotify-transfer.bat`
3. Follow the on-screen instructions

### Linux/Mac

1. Download all files to the same folder
2. Open terminal in the files folder
3. Make the script executable: `chmod +x run-spotify-transfer.sh`
4. Run the script: `./run-spotify-transfer.sh`
5. Follow the on-screen instructions

## Setup

On first run, you'll need to configure access to both APIs:

### Spotify API

1. Go to https://developer.spotify.com/dashboard/
2. Log in with your Spotify account
3. Create a new application:
   - Click "Create app"
   - Enter a name (e.g., "SpotifyToYTMusic")
   - Enter a description
   - Enter `http://localhost` as the "Redirect URI"
   - Select "Web API" as the API to use
   - Accept the terms of service
4. In the app dashboard, copy the "Client ID" and "Client Secret"
5. Enter these values when prompted by the script

### YouTube Music (Detailed Guide)

1. When the script asks "Enter the path to save the authentication file", simply press ENTER to use the default path

2. **Important: Instructions to get authentication headers:**
   - Open Firefox (Firefox is required)
   - Go to https://music.youtube.com and make sure you're logged in
   - Press F12 to open Developer Tools
   - Select the "Network" tab
   - Reload the page (F5)
   - **Select any request to music.youtube.com in the list** (preferably the first one)
   - **Right-click on the request and select "Copy" → "Copy Request Headers"**
   
   ![Example of how to copy headers](https://i.imgur.com/IYjTUGI.png)
   
3. Return to the terminal/command prompt window where the script is running
4. **Paste the copied headers** and press:
   - Windows: press ENTER, then CTRL+Z, then ENTER again
   - Mac/Linux: press ENTER, then CTRL+D, then ENTER again

If you have problems with this authentication method, you can alternatively:
1. Log in to YouTube Music in the browser
2. Open developer tools (F12)
3. Go to the "Application" or "Storage" tab
4. Manually copy the cookies from the music.youtube.com domain

## Usage

After the initial configuration, you can run the script in one of the following ways:

### With the graphical interface

- Windows: double-click on `run-spotify-transfer.bat`
- Linux/Mac: double-click on `run-spotify-transfer.sh` (if your system supports it) or run it from terminal

### With the URL as a parameter

- Windows: `run-spotify-transfer.bat https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`
- Linux/Mac: `./run-spotify-transfer.sh https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`

## Advanced Options

If you want to use additional options, you can run the Python script directly:

```
python spotify_to_youtube.py PLAYLIST_URL [options]
```

Available options:
- `--name`: Custom name for the YouTube Music playlist
- `--privacy`: Set the playlist privacy ("PUBLIC", "PRIVATE", "UNLISTED")
- `--config`: Custom path for the configuration file

Example:
```
python spotify_to_youtube.py https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M --name "My playlist" --privacy PUBLIC
```

## Troubleshooting

### Error during YouTube Music authentication

If you receive errors during authentication:
1. Make sure you're logged in to YouTube Music in the browser
2. Try using the browser in normal mode (not incognito)
3. Temporarily disable any ad-blockers or VPNs
4. If you continue to have problems, try using Chrome instead of Firefox (modify the README based on the browser used)

### Error "No module named 'spotipy'" or "No module named 'ytmusicapi'"

Run manually:
```
pip install spotipy ytmusicapi
```

### Python not found or wrong version

The scripts will automatically search for Python on your system. If you have problems:

1. Verify that Python 3.8+ is installed with `python --version` or `python3 --version`
2. If you have multiple versions installed, manually specify the path in the .bat/.sh file or use:
   ```
   /complete/path/to/python spotify_to_youtube.py PLAYLIST_URL
   ```

### Saved credentials

Credentials are saved in:
- Spotify API: in the configuration file (`~/spotify_ytmusic_config.json`)
- YouTube Music: in the authentication file (`headers_auth.json` in the script folder)

To reset the authentication, delete these files.