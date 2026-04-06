"""
EarGuard Volume Bridge - Live OS Sync
Run this FIRST, then run earguard.py in a second terminal.

Install once:  pip install pycaw comtypes
Run:           python volume_tracker.py
"""

import time
from pathlib import Path
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

SCRIPT_DIR = Path(__file__).parent.resolve()
OUT_FILE   = SCRIPT_DIR / "current_volume.txt"

def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return int(round(volume.GetMasterVolumeLevelScalar() * 100))

def write_vol(v):
    OUT_FILE.write_text(str(v))
    bar = "█" * (v // 5) + "░" * (20 - v // 5)
    print(f"\r  Volume: {v:3d}%  [{bar}]", end="", flush=True)

print("=" * 45)
print("  EarGuard Volume Bridge (Pycaw)")
print("=" * 45)
print(f"  Writing to: {OUT_FILE}")
print()
print("  Live tracking OS master volume...")
print("  Ctrl+C to stop.")
print()

try:
    last_vol = -1
    while True:
        try:
            current_vol = get_volume()
            if current_vol != last_vol:
                write_vol(current_vol)
                last_vol = current_vol
        except Exception:
            pass  # Ignore temporary errors retrieving volume
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n  Bridge stopped. Cleaning up...")
    if OUT_FILE.exists():
        OUT_FILE.unlink()
    print("  Done.")