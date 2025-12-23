#!/usr/bin/env python3
"""
Radio Recorder - Rádio do Concelho de Mafra (105.6 MHz)
Records 1 hour of audio starting at 10:00 AM sharp
"""

import subprocess
import sys
from datetime import datetime, timedelta
import time
import os
import argparse

# Configuration
STREAM_URL = "https://centova.radio.com.pt/proxy/551?mp=/stream"
DURATION_SECONDS = 3600  # 1 hour (default)
TARGET_HOUR = 10
TARGET_MINUTE = 0

def get_output_filename(test_mode=False):
    """Generate output filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "TEST_radio_mafra" if test_mode else "radio_mafra"
    return f"{prefix}_{timestamp}.mp3"

def wait_until_target_time(test_mode=False, test_wait_minutes=2):
    """Wait until target time (10:00 AM or test mode: 2 minutes from now)"""
    now = datetime.now()
    
    if test_mode:
        # Test mode: wait 2 minutes from now
        target = now + timedelta(minutes=test_wait_minutes)
        target = target.replace(second=0, microsecond=0)
    else:
        # Production mode: wait until 10:00 AM
        target = now.replace(hour=TARGET_HOUR, minute=TARGET_MINUTE, second=0, microsecond=0)
        
        # If target time has passed today, inform the user
        if now >= target:
            print(f"⚠️  10:00 AM has already passed today (current time: {now.strftime('%H:%M:%S')})")
            response = input("Start recording immediately? (y/n): ").strip().lower()
            if response == 'y':
                return True
            else:
                print("Recording cancelled.")
                sys.exit(0)
    
    wait_seconds = (target - now).total_seconds()
    print(f"📅 Current time: {now.strftime('%H:%M:%S')}")
    print(f"⏰ Recording scheduled for: {target.strftime('%H:%M:%S')}")
    print(f"⏳ Waiting {int(wait_seconds // 60)} minutes and {int(wait_seconds % 60)} seconds...")
    
    # Wait with countdown updates
    while True:
        now = datetime.now()
        remaining = (target - now).total_seconds()
        
        if remaining <= 0:
            break
        
        if remaining > 60:
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            print(f"   ⏳ {mins}m {secs}s remaining...", end='\r')
            time.sleep(10)  # Update every 10 seconds for test mode responsiveness
        else:
            print(f"   ⏳ {int(remaining)}s remaining...    ", end='\r')
            time.sleep(1)
    
    print("\n")
    return True

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def record_stream(output_file, duration_seconds):
    """Record the radio stream using ffmpeg"""
    print(f"🎙️  Starting recording...")
    print(f"📻 Station: Rádio do Concelho de Mafra (105.6 MHz)")
    print(f"🔗 Stream: {STREAM_URL}")
    if duration_seconds < 60:
        print(f"⏱️  Duration: {duration_seconds} seconds")
    else:
        print(f"⏱️  Duration: {duration_seconds // 60} minutes")
    print(f"💾 Output: {output_file}")
    print("-" * 50)
    
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)
    print(f"▶️  Recording started at: {start_time.strftime('%H:%M:%S')}")
    print(f"⏹️  Recording will end at: {end_time.strftime('%H:%M:%S')}")
    print("-" * 50)
    
    cmd = [
        "ffmpeg",
        "-y",                          # Overwrite output file if exists
        "-i", STREAM_URL,              # Input stream URL
        "-t", str(duration_seconds),   # Duration in seconds
        "-acodec", "libmp3lame",       # MP3 codec
        "-ab", "192k",                 # Bitrate 192kbps for good quality
        "-ar", "44100",                # Sample rate
        "-ac", "2",                    # Stereo
        output_file
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor the process
        while process.poll() is None:
            elapsed = (datetime.now() - start_time).total_seconds()
            remaining = duration_seconds - elapsed
            
            if remaining > 0:
                if duration_seconds >= 60:
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    progress = (elapsed / duration_seconds) * 100
                    print(f"   🔴 Recording... {progress:.1f}% complete | {mins}m {secs}s remaining", end='\r', flush=True)
                else:
                    progress = (elapsed / duration_seconds) * 100
                    print(f"   🔴 Recording... {progress:.1f}% complete | {int(remaining)}s remaining", end='\r', flush=True)
            
            time.sleep(1 if duration_seconds < 60 else 5)
        
        # Clear the progress line completely and move to new line
        print(" " * 80, end='\r', flush=True)
        print(flush=True)
        
        if process.returncode == 0:
            file_size = os.path.getsize(output_file)
            if file_size > 1024 * 1024:
                file_size_mb = file_size / (1024 * 1024)
                size_str = f"{file_size_mb:.2f} MB"
            else:
                file_size_kb = file_size / 1024
                size_str = f"{file_size_kb:.2f} KB"
            print("=" * 50, flush=True)
            print(f"✅ Recording completed successfully!", flush=True)
            print(f"📁 File: {output_file}", flush=True)
            print(f"📊 Size: {size_str}", flush=True)
            print("=" * 50, flush=True)
            return True
        else:
            stderr_output = process.stderr.read()
            print(f"❌ Recording failed!", flush=True)
            print(f"Error: {stderr_output}", flush=True)
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording interrupted by user", flush=True)
        process.terminate()
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size > 1024 * 1024:
                file_size_mb = file_size / (1024 * 1024)
                size_str = f"{file_size_mb:.2f} MB"
            else:
                file_size_kb = file_size / 1024
                size_str = f"{file_size_kb:.2f} KB"
            print(f"📁 Partial recording saved: {output_file} ({size_str})", flush=True)
        return False
    except Exception as e:
        print(f"❌ Error during recording: {e}", flush=True)
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Record radio stream')
    parser.add_argument('--test', action='store_true', 
                       help='Test mode: record 1 minute starting in 2 minutes')
    args = parser.parse_args()
    
    # Set test mode parameters
    test_mode = args.test
    if test_mode:
        duration_seconds = 60  # 1 minute for test
        test_wait_minutes = 2
        print("=" * 50)
        print("🧪 TEST MODE - Rádio do Concelho de Mafra")
        print("=" * 50)
        print("⚠️  This is a TEST: Recording 1 minute starting in 2 minutes")
    else:
        duration_seconds = DURATION_SECONDS  # 1 hour for production
        test_wait_minutes = 0
        print("=" * 50)
        print("🎵 RADIO RECORDER - Rádio do Concelho de Mafra")
        print("=" * 50)
    print()
    
    # Check ffmpeg
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed!")
        print("   Install it with: brew install ffmpeg")
        sys.exit(1)
    
    print("✅ ffmpeg found")
    
    # Wait until target time
    wait_until_target_time(test_mode=test_mode, test_wait_minutes=test_wait_minutes)
    
    # Generate output filename
    output_file = get_output_filename(test_mode=test_mode)
    
    # Start recording with appropriate duration
    record_stream(output_file, duration_seconds)

if __name__ == "__main__":
    main()

