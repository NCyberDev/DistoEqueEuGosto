#!/bin/bash
# Script to download and install ffmpeg for macOS

echo "📥 Downloading ffmpeg for macOS..."

# Create a local bin directory
mkdir -p ~/bin
cd ~/bin

# Check if we're on Apple Silicon or Intel
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo "🍎 Detected Apple Silicon (M1/M2/M3)"
    FFMPEG_URL="https://evermeet.cx/ffmpeg/ffmpeg-7.0.zip"
else
    echo "💻 Detected Intel Mac"
    FFMPEG_URL="https://evermeet.cx/ffmpeg/ffmpeg-7.0.zip"
fi

# Download ffmpeg
echo "⬇️  Downloading from evermeet.cx..."
curl -L -o ffmpeg.zip "$FFMPEG_URL"

if [ $? -eq 0 ]; then
    echo "✅ Download complete"
    echo "📦 Extracting..."
    unzip -q -o ffmpeg.zip
    rm ffmpeg.zip
    
    # Make executable
    chmod +x ffmpeg
    
    # Add to PATH in current session
    export PATH="$HOME/bin:$PATH"
    
    echo ""
    echo "✅ ffmpeg installed to ~/bin/ffmpeg"
    echo ""
    echo "To make it permanent, add this to your ~/.zshrc:"
    echo "  export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
    echo "Testing installation..."
    ~/bin/ffmpeg -version | head -3
else
    echo "❌ Download failed. Trying alternative method..."
    echo ""
    echo "Please download manually from:"
    echo "https://evermeet.cx/ffmpeg/"
    echo ""
    echo "Or visit: https://ffmpeg.org/download.html"
fi

