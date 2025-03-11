@echo off
setlocal enabledelayedexpansion

echo Spotify to YouTube Music Transfer
echo =================================

:: Ottieni il percorso in cui si trova questo batch file
cd /d "%~dp0"
echo Directory di lavoro: %CD%

:: Percorso assoluto per Python 3.9
set PYTHON_PATH=C:\Users\roves\AppData\Local\Programs\Python\Python39\python.exe

:: Se non esiste Python 3.9 nel percorso specifico, cerca altre versioni
if not exist "%PYTHON_PATH%" (
    for %%P in (
        "C:\Python39\python.exe"
        "C:\Program Files\Python39\python.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    ) do (
        if exist %%P (
            set PYTHON_PATH=%%P
            goto :found_python
        )
    )
    
    echo Python non trovato nei percorsi standard.
    echo Inserisci il percorso completo a python.exe:
    set /p PYTHON_PATH=
    
    if not exist "!PYTHON_PATH!" (
        echo Il percorso specificato non esiste.
        pause
        exit /b 1
    )
)

:found_python
echo Usando Python: %PYTHON_PATH%

:: Verifica che il file script esista
if not exist "spotify_to_youtube.py" (
    echo ERRORE: Il file spotify_to_youtube.py non è stato trovato nella cartella corrente: %CD%
    echo Assicurati che questo file .bat sia nella stessa cartella di spotify_to_youtube.py
    pause
    exit /b 1
)

:: Installa le dipendenze
echo Installazione dipendenze...
"%PYTHON_PATH%" -m pip install spotipy ytmusicapi

:: Chiedi URL playlist o usa quello passato come argomento
if "%~1"=="" (
    set /p PLAYLIST_URL=Inserisci URL playlist Spotify: 
) else (
    set PLAYLIST_URL=%~1
)

:: Esegui script
echo.
echo Esecuzione script...
"%PYTHON_PATH%" spotify_to_youtube.py %PLAYLIST_URL%

echo.
if %ERRORLEVEL% neq 0 (
    echo Si è verificato un errore durante l'esecuzione dello script.
) else (
    echo Script completato.
)

pause