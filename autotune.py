from os import rename, remove, path
from download import download
from pathHelper import *
from subprocessHelper import *
import subprocess, random


loglevel = "error"

def getDur(f):
    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", f], capture_output=True, text=True)
        return float(result.stdout.strip())
    except Exception:
        return 0.0

def autotune(base, over, filename, strength = 75, executableName = "./autotune.exe", reformatAudio = True, hz = 48000):
    strength = max(1, min(strength, 512))
    if reformatAudio:
        baseDur = getDur(base)
        loud_run(["ffmpeg", "-y", "-hide_banner", "-loglevel", loglevel, "-i", base, "-ac", "1", "-ar", str(hz), base := chExt(addPrefix(absPath(base), 'AT_'), 'wav')])
        loud_run(["ffmpeg", "-y", "-hide_banner", "-loglevel", loglevel, "-i", over, "-ac", "1", "-ar", str(hz), '-t', str(baseDur), over := chExt(addPrefix(absPath(over), 'AT_'), 'wav')])
    
    try:
        # Check if it's an exe and we are on linux
        if executableName.endswith('.exe'):
             print(f"Skipping autotune: .exe binaries are not supported on this environment.")
        else:
             silent_run([executableName, '-b', str(strength), base, over, filename])
    except Exception as e:
        print(f"Failed to execute autotune: {e}")
        
    if reformatAudio:
        if path.exists(base): remove(base)
        if path.exists(over): remove(over)

randDigits = lambda: str(random.random()).replace('.', '') 

def autotuneURL(filename, URL, replaceOriginal = True, video = True, executableName = "./autotune.exe"):
        directory = path.split(path.abspath(filename))[0]
        downloadName = f"{directory}/download_{randDigits()}.wav"
        result = download(downloadName, URL, video = False, duration = 2 * 60)
        if result:
                wavName = f'{directory}/vidAudio_{randDigits()}.wav'
                if video:
                        loud_run(["ffmpeg", "-hide_banner", "-loglevel", loglevel, "-i", filename, "-ac", "1", wavName])
                else:
                        rename(filename, wavName)
                autotuneName = f'{directory}/autotune_{randDigits()}.wav'
                autotune(wavName, downloadName, autotuneName, executableName = executableName)
                
                if not path.exists(autotuneName):
                    print(f"Autotune failed: {autotuneName} was not created.")
                    # Return original filename to indicate failure but allow processing to continue
                    # Cleanup first
                    remove(downloadName)
                    remove(wavName)
                    return filename if replaceOriginal else filename

                # SUCCESS PATH - perform cleanup after successful autotune
                remove(downloadName)
                remove(wavName)
                exportName = f"{directory}/{randDigits()}{path.splitext(filename)[1]}"
                if video:
                        loud_run(["ffmpeg", "-hide_banner", "-loglevel", loglevel, "-i", filename, "-i", autotuneName, "-map", "0:v", "-map", "1:a", "-ac", "1", exportName])
                        remove(autotuneName)
                else:
                        rename(autotuneName, exportName)
                
                if replaceOriginal:
                        if video:
                                remove(filename)
                        rename(exportName, filename)
                        return filename
                return exportName
        else:
                return [f"Error downloading {URL}"]