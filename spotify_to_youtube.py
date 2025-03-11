import os
import re
import json
import time
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic


class SpotifyToYTMusic:
    def __init__(self, config_path=None):
        """Inizializza le API di Spotify e YouTube Music."""
        self.config_path = config_path or Path.home() / "spotify_ytmusic_config.json"
        self.config = self._load_config()
        
        # Inizializza Spotify API
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.config["spotify"]["client_id"],
            client_secret=self.config["spotify"]["client_secret"]
        )
        self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Inizializza YouTube Music API
        self.ytmusic = YTMusic(self.config["youtube"]["headers_file"])
    
    def _load_config(self):
        """Carica la configurazione o richiede la configurazione all'utente."""
        if not os.path.exists(self.config_path):
            return self._setup_config()
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _setup_config(self):
        """Configura le credenziali per Spotify e YouTube Music."""
        config = {
            "spotify": {},
            "youtube": {}
        }
        
        print("--- Configurazione Spotify API ---")
        print("Registra un'applicazione su https://developer.spotify.com/dashboard/")
        config["spotify"]["client_id"] = input("Inserisci Client ID Spotify: ")
        config["spotify"]["client_secret"] = input("Inserisci Client Secret Spotify: ")
        
        print("\n--- Configurazione YouTube Music API ---")
        print("Seguire le istruzioni per generare i cookie di autenticazione")
        headers_file = input("Inserisci il percorso dove salvare il file di autenticazione (default: headers_auth.json): ") or "headers_auth.json"
        
        # Crea il file di autenticazione YTMusic - Correzione per ytmusicapi 1.10.2
        # La funzione setup() non accetta open_browser come parametro
        import ytmusicapi
        ytmusicapi.setup(filepath=headers_file)
        config["youtube"]["headers_file"] = headers_file
        
        # Salva la configurazione
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configurazione salvata in {self.config_path}")
        return config
    
    def extract_playlist_id(self, spotify_url):
        """Estrae l'ID della playlist dall'URL di Spotify."""
        match = re.search(r"playlist/([a-zA-Z0-9]+)", spotify_url)
        if match:
            return match.group(1)
        raise ValueError("URL della playlist Spotify non valido")
    
    def get_spotify_playlist(self, playlist_url):
        """Ottiene i dettagli della playlist Spotify."""
        playlist_id = self.extract_playlist_id(playlist_url)
        
        # Ottieni le informazioni sulla playlist
        playlist = self.spotify.playlist(playlist_id)
        name = playlist["name"]
        description = playlist["description"]
        
        # Ottieni tutte le tracce (gestisce playlist con più di 100 tracce)
        tracks = []
        results = playlist["tracks"]
        tracks.extend(results["items"])
        
        while results["next"]:
            results = self.spotify.next(results)
            tracks.extend(results["items"])
        
        print(f"Playlist '{name}' contiene {len(tracks)} tracce")
        return {
            "name": name,
            "description": description,
            "tracks": tracks
        }
    
    def find_on_youtube(self, track):
        """Cerca una traccia Spotify su YouTube Music."""
        if not track["track"]:
            return None
            
        # Estrai le informazioni sulla traccia
        track_name = track["track"]["name"]
        artists = [artist["name"] for artist in track["track"]["artists"]]
        artist_name = artists[0]  # Prendi solo il primo artista per la ricerca
        
        # Crea la query di ricerca
        query = f"{track_name} {artist_name}"
        
        # Cerca su YouTube Music
        results = self.ytmusic.search(query, filter="songs")
        
        if not results:
            print(f"Non trovato: {query}")
            return None
        
        # Prendi il primo risultato
        return results[0]["videoId"]
    
    def transfer_playlist(self, playlist_url, new_name=None, privacy="PRIVATE"):
        """Trasferisce una playlist Spotify a YouTube Music."""
        # Ottieni i dettagli della playlist
        spotify_playlist = self.get_spotify_playlist(playlist_url)
        playlist_name = new_name or spotify_playlist["name"]
        
        # Cerca ogni traccia su YouTube Music
        print("Ricerca tracce su YouTube Music...")
        video_ids = []
        for i, track in enumerate(spotify_playlist["tracks"]):
            video_id = self.find_on_youtube(track)
            if video_id:
                video_ids.append(video_id)
            
            # Mostra il progresso ogni 10 tracce
            if (i + 1) % 10 == 0:
                print(f"Progresso: {i + 1}/{len(spotify_playlist['tracks'])}")
        
        print(f"Trovate {len(video_ids)}/{len(spotify_playlist['tracks'])} tracce")
        
        # Crea la playlist su YouTube Music
        if video_ids:
            result = self.ytmusic.create_playlist(
                title=playlist_name,
                description=f"Importata da Spotify: {spotify_playlist['description']}",
                privacy_status=privacy,
                video_ids=video_ids
            )
            print(f"Playlist creata: https://music.youtube.com/playlist?list={result}")
            return result
        else:
            print("Nessuna traccia trovata. Playlist non creata.")
            return None


def main():
    """Funzione principale per l'esecuzione da linea di comando."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Trasferisci playlist da Spotify a YouTube Music")
    parser.add_argument("playlist_url", help="URL della playlist Spotify da trasferire")
    parser.add_argument("--name", help="Nome personalizzato per la playlist YouTube Music")
    parser.add_argument("--privacy", choices=["PUBLIC", "PRIVATE", "UNLISTED"], default="PRIVATE",
                        help="Impostazioni privacy della playlist (default: PRIVATE)")
    parser.add_argument("--config", help="Percorso del file di configurazione personalizzato")
    
    args = parser.parse_args()
    
    try:
        transfer = SpotifyToYTMusic(config_path=args.config)
        transfer.transfer_playlist(args.playlist_url, args.name, args.privacy)
    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()