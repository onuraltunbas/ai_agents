#!/usr/bin/env bash
# ==============================================================================
# ONUR AI Multi-Agent Ecosystem - 1-Click Installer
# ==============================================================================
set -e

echo "🚀 Installing ONUR AI Multi-Agent System..."

# 1. Check & Install System Dependencies
echo "📦 Installing global verification & dev dependencies..."
sudo apt update -y && sudo apt install -y curl git python3 python3-pip gcc g++ make

# 2. Install Python Verification Tools Globally
echo "🔬 Setting up Ruff, Mypy, Pytest globally..."
python3 -m pip install --break-system-packages --user pytest ruff mypy numpy

# 3. Check / Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "🦙 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 4. Pull Model & Configure Modelfile
echo "🧠 Setting up local Qwen3-Coder 30B model with 64K context & thermal optimization..."
ollama pull qwen3-coder:30b
ollama pull nomic-embed-text

cat << 'MODEL_EOF' > /tmp/Modelfile-onur-ai
FROM qwen3-coder:30b
PARAMETER num_ctx 65536
PARAMETER num_thread 6
MODEL_EOF
ollama create qwen3-coder:30b -f /tmp/Modelfile-onur-ai
rm -f /tmp/Modelfile-onur-ai

# 5. Install OpenCode CLI
if ! command -v opencode &> /dev/null; then
    echo "⚡ Installing OpenCode CLI engine..."
    curl -fsSL https://opencode.ai/install | bash
fi

# 6. Copy Configurations, Prompts & Skills
echo "📁 Configuring agents & skills..."
mkdir -p ~/.config/opencode/skills ~/.onur_ai

cp config/opencode.jsonc ~/.config/opencode/opencode.jsonc
cp config/instructions.md ~/.config/opencode/instructions.md
cp -r skills/* ~/.config/opencode/skills/
cp -r core/ ~/.onur_ai/core/

# 7. Create CLI Launchers
mkdir -p ~/.local/bin
cp bin/* ~/.local/bin/
chmod +x ~/.local/bin/*

# Ensure ~/.local/bin and ~/.opencode/bin are in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo "================================================================"
echo "🎉 ONUR AI System Successfully Installed & Ready!"
echo "================================================================"
echo "Commands you can now use anywhere:"
echo "  cooker    -> Master Coding & Systems Agent"
echo "  selimbey  -> Master UI/UX & Web Design Agent"
echo "  sohbet    -> Personal Mentor, Chat & Life Agent"
echo "  doktor    -> Evidence-Based Medical & Biohack Agent"
echo "  ironman   -> Supreme Meta-Orchestrator"
echo "================================================================"
