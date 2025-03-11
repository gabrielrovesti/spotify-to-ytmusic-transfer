#!/bin/bash

echo "Spotify to YouTube Music Transfer"
echo "================================="

# Cambia directory alla posizione dello script
cd "$(dirname "$0")"
echo "Directory di lavoro: $(pwd)"

# Trova Python 3.8+
PYTHON_CMD=""
for cmd in python3 python python3.9 python3.10 python3.11 python3.12; do
    if command -v $cmd &> /dev/null; then
        version=$($cmd -c 'import sys; print(sys.version_info.major * 10 + sys.version_info.minor)')
        if [ "$version" -ge 38 ]; then
            PYTHON_CMD=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Errore: Non è stata trovata una versione di Python 3.8+ installata."
    echo "Installa Python 3.8 o superiore da https://www.python.org/downloads/"
    exit 1
fi

echo "Usando Python: $($PYTHON_CMD --version)"

# Verifica che il file script esista
if [ ! -f "spotify_to_youtube.py" ]; then
    echo "ERRORE: Il file spotify_to_youtube.py non è stato trovato nella directory corrente: $(pwd)"
    echo "Assicurati che questo script sia nella stessa directory di spotify_to_youtube.py"
    read -p "Premi Invio per continuare..."
    exit 1
fi

# Installa le dipendenze
echo "Installazione dipendenze..."
$PYTHON_CMD -m pip install spotipy ytmusicapi

# Chiedi URL playlist o usa quello passato come argomento
if [ $# -eq 0 ]; then
    read -p "Inserisci URL playlist Spotify: " PLAYLIST_URL
else
    PLAYLIST_URL="$1"
fi

# Esegui script
echo
echo "Esecuzione script..."
$PYTHON_CMD spotify_to_youtube.py "$PLAYLIST_URL"

echo
if [ $? -ne 0 ]; then
    echo "Si è verificato un errore durante l'esecuzione dello script."
else
    echo "Script completato."
fi

read -p "Premi Invio per continuare..."