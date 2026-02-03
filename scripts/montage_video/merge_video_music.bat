@echo off
REM ============================================================
REM Exemple : associer une vidéo de démo et une musique pour LinkedIn
REM Nécessite FFmpeg dans le PATH (https://ffmpeg.org/download.html)
REM ============================================================

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

set VIDEO=demo.mp4
set MUSIC=musique.mp3
set OUTPUT=demo_avec_musique.mp4

if not exist "%VIDEO%" (
  echo Fichier manquant: %VIDEO%
  echo Placez votre video de demo ici et nommez-la demo.mp4
  pause
  exit /b 1
)

if not exist "%MUSIC%" (
  echo Fichier manquant: %MUSIC%
  echo Placez votre musique (MP3) ici et nommez-la musique.mp3
  pause
  exit /b 1
)

echo Fusion video + musique en cours...
echo Video: %VIDEO%
echo Musique: %MUSIC%
echo Sortie: %OUTPUT%
echo.

REM Mixer son original video (20%%) + musique (40%%) ; si la video n'a pas de son, utiliser seulement la musique
ffmpeg -y -i "%VIDEO%" -i "%MUSIC%" -filter_complex "[0:a]volume=0.2[a1];[1:a]volume=0.4[a2];[a1][a2]amix=inputs=2:duration=shortest[aout]" -map 0:v -map "[aout]" -c:v copy -shortest "%OUTPUT%" 2>nul

if errorlevel 1 (
  REM Si la video n'a pas de piste audio, ajouter seulement la musique
  echo La video n a pas de son, ajout de la musique uniquement...
  ffmpeg -y -i "%VIDEO%" -i "%MUSIC%" -filter_complex "[1:a]volume=0.5[aout]" -map 0:v -map "[aout]" -c:v copy -shortest "%OUTPUT%"
)

if exist "%OUTPUT%" (
  echo.
  echo Termine : %OUTPUT%
) else (
  echo Erreur lors de la creation du fichier.
)

pause
