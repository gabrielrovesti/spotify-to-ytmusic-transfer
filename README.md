# Spotify to YouTube Music Transfer

Uno script semplice per trasferire le tue playlist da Spotify a YouTube Music.

## Requisiti

- Python 3.8 o superiore (testato con Python 3.9)
- Account Spotify
- Account YouTube/Google
- Browser Firefox (necessario per l'autenticazione a YouTube Music)

## Istruzioni Rapide

### Windows

1. Scarica tutti i file nella stessa cartella
2. Fai doppio clic su `run-spotify-transfer.bat`
3. Segui le istruzioni a schermo

### Linux/Mac

1. Scarica tutti i file nella stessa cartella
2. Apri il terminale nella cartella dei file
3. Rendi lo script eseguibile: `chmod +x run-spotify-transfer.sh`
4. Esegui lo script: `./run-spotify-transfer.sh`
5. Segui le istruzioni a schermo

## Setup

Al primo avvio, dovrai configurare l'accesso alle API:

### Spotify API

1. Vai su https://developer.spotify.com/dashboard/
2. Accedi con il tuo account Spotify
3. Crea una nuova applicazione:
   - Clicca su "Create app"
   - Inserisci un nome (es. "SpotifyToYTMusic")
   - Inserisci una descrizione
   - Inserisci `http://localhost` come "Redirect URI"
   - Seleziona "Web API" come API da utilizzare
   - Accetta i termini di servizio
4. Nella dashboard dell'app, copia il "Client ID" e "Client Secret"
5. Inserisci questi valori quando richiesti dallo script

### YouTube Music (Guida dettagliata)

1. Quando lo script chiede "Inserisci il percorso dove salvare il file di autenticazione", premi semplicemente INVIO per usare il percorso predefinito

2. **Importante: Istruzioni per ottenere le intestazioni di autenticazione:**
   - Apri Firefox (è necessario usare Firefox)
   - Vai a https://music.youtube.com e assicurati di aver effettuato l'accesso
   - Premi F12 per aprire gli Strumenti di sviluppo
   - Seleziona la scheda "Rete" (Network)
   - Ricarica la pagina (F5)
   - **Seleziona qualsiasi richiesta verso music.youtube.com nella lista** (preferibilmente la prima)
   - **Fai clic destro sulla richiesta e seleziona "Copia" → "Copia header richiesta"** (o "Copy Request Headers")
   
   ![Esempio di come copiare gli headers](https://i.imgur.com/IYjTUGI.png)
   
3. Torna alla finestra del terminale/prompt dei comandi dove è in esecuzione lo script
4. **Incolla le intestazioni copiate** e premi:
   - Windows: premi INVIO, poi CTRL+Z, poi INVIO di nuovo
   - Mac/Linux: premi INVIO, poi CTRL+D, poi INVIO di nuovo

Se hai problemi con questo metodo di autenticazione, puoi in alternativa:
1. Accedere a YouTube Music nel browser
2. Aprire gli strumenti di sviluppo (F12)
3. Andare nella scheda "Applicazione" o "Storage"
4. Copiare manualmente i cookie dal dominio music.youtube.com

## Utilizzo

Dopo la configurazione iniziale, puoi eseguire lo script in uno dei seguenti modi:

### Con l'interfaccia grafica

- Windows: doppio clic su `run-spotify-transfer.bat`
- Linux/Mac: doppio clic su `run-spotify-transfer.sh` (se il sistema lo supporta) o eseguilo da terminale

### Con l'URL come parametro

- Windows: `run-spotify-transfer.bat https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`
- Linux/Mac: `./run-spotify-transfer.sh https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`

## Opzioni avanzate

Se vuoi utilizzare opzioni aggiuntive, puoi eseguire direttamente lo script Python:

```
python spotify_to_youtube.py URL_PLAYLIST [opzioni]
```

Opzioni disponibili:
- `--name`: Nome personalizzato per la playlist su YouTube Music
- `--privacy`: Imposta la privacy della playlist ("PUBLIC", "PRIVATE", "UNLISTED")
- `--config`: Percorso personalizzato per il file di configurazione

Esempio:
```
python spotify_to_youtube.py https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M --name "La mia playlist" --privacy PUBLIC
```

## Risoluzione problemi

### Errore durante l'autenticazione a YouTube Music

Se ricevi errori durante l'autenticazione:
1. Assicurati di essere loggato a YouTube Music nel browser
2. Prova a usare il browser in modalità normale (non in incognito)
3. Disabilita temporaneamente eventuali estensioni di blocco pubblicità o VPN
4. Se continui ad avere problemi, prova a usare Chrome anziché Firefox (modifica il README in base al browser utilizzato)

### Errore "No module named 'spotipy'" o "No module named 'ytmusicapi'"

Esegui manualmente:
```
pip install spotipy ytmusicapi
```

### Python non trovato o versione sbagliata

Gli script cercheranno automaticamente Python sul tuo sistema. Se hai problemi:

1. Verifica che Python 3.8+ sia installato con `python --version` o `python3 --version`
2. Se hai più versioni installate, specifica manualmente il percorso nel file .bat/.sh o usa:
   ```
   /percorso/completo/a/python spotify_to_youtube.py URL_PLAYLIST
   ```

### Credenziali salvate

Le credenziali vengono salvate in:
- Spotify API: nel file di configurazione (`~/spotify_ytmusic_config.json`)
- YouTube Music: nel file di autenticazione (`headers_auth.json` nella cartella dello script)

Per reimpostare l'autenticazione, elimina questi file.