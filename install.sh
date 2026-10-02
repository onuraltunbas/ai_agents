#!/usr/bin/env bash
# ==============================================================================
# AI AGENTS - Autonomous Multi-Agent Ecosystem - 1-Click Complete Installer
# ==============================================================================
# Bu betik sıfır bir Linux/Ubuntu makinede yerel çoklu ajan ekosistemini (Ollama,
# Qwen3-Coder 30B, OpenCode CLI, tüm 6 ajan, 14 skill ve SQLite hafızayı)
# birebir eksiksiz olarak kurar ve kullanıma hazır hale getirir.
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "🚀 Installing Autonomous Multi-Agent Ecosystem from: $SCRIPT_DIR"

# 1. Sistem Bağımlılıklarını Kur
echo ""
echo "📦 [1/8] Installing system dependencies (curl, git, python3, gcc, g++, sqlite3)..."
if command -v apt-get &> /dev/null; then
    sudo apt update -y
    sudo apt install -y curl git python3 python3-pip python3-venv gcc g++ make sqlite3
else
    echo "⚠️ Non-Debian/Ubuntu system detected. Please ensure curl, git, python3, gcc, g++, and sqlite3 are installed."
fi

# 2. Python Doğrulama ve Test Araçlarını Kur
echo ""
echo "🔬 [2/8] Installing Python verification tools (Ruff, Mypy, Pytest, Numpy)..."
python3 -m pip install --break-system-packages --user pytest ruff mypy numpy 2>/dev/null || \
python3 -m pip install --user pytest ruff mypy numpy

# 3. Ollama Kurulumu ve Servis Başlatma
echo ""
echo "🦙 [3/8] Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "⬇️ Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Ollama servisinin ayakta olduğundan emin ol
echo "🔄 Verifying Ollama service status..."
if command -v systemctl &> /dev/null && systemctl list-unit-files | grep -q "ollama.service"; then
    sudo systemctl enable --now ollama 2>/dev/null || true
fi

# Servisin yanıt vermesini bekle (maksimum 15 sn)
for i in {1..15}; do
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama service is active and listening on port 11434."
        break
    fi
    echo "⏳ Waiting for Ollama daemon to initialize... ($i/15)"
    sleep 1
done

# 4. Modelleri İndir ve 32K Context Modelfile ile Yapılandır
echo ""
echo "🧠 [4/8] Pulling and configuring local models (Qwen3-Coder 30B & Nomic Embed)..."
ollama pull qwen3-coder:30b
ollama pull nomic-embed-text

if [ -f "$SCRIPT_DIR/Modelfile" ]; then
    echo "⚙️ Applying custom Modelfile (32K Context, 6 Threads)..."
    ollama create qwen3-coder:30b -f "$SCRIPT_DIR/Modelfile"
fi

# 5. OpenCode CLI Kurulumu
echo ""
echo "⚡ [5/8] Checking OpenCode CLI..."
if ! command -v opencode &> /dev/null; then
    echo "⬇️ Installing OpenCode CLI engine..."
    curl -fsSL https://opencode.ai/install | bash
fi

# 6. Konfigürasyon, Ajan Promptları ve Becerileri (Skills) Kopyala
echo ""
echo "📁 [6/8] Configuring agents, skills, instructions and core modules..."
mkdir -p "$HOME/.config/opencode/skills" "$HOME/.local_ai/core"

cp "$SCRIPT_DIR/config/opencode.jsonc" "$HOME/.config/opencode/opencode.jsonc"
cp "$SCRIPT_DIR/config/instructions.md" "$HOME/.config/opencode/instructions.md"
cp -r "$SCRIPT_DIR/skills/"* "$HOME/.config/opencode/skills/"
cp -r "$SCRIPT_DIR/core/"* "$HOME/.local_ai/core/"

# 7. SQLite Kalıcı Hafızayı (Memory) Başlat
echo ""
echo "💾 [7/8] Seeding Long-Term Memory SQLite database with default preferences..."
python3 "$SCRIPT_DIR/core/seed_memory.py"

# 8. Terminal Kısayollarını (CLI Launchers) Kur ve PATH'e Ekle
echo ""
echo "🔧 [8/8] Installing CLI launchers into ~/.local/bin..."
mkdir -p "$HOME/.local/bin"
cp "$SCRIPT_DIR/bin/"* "$HOME/.local/bin/"
chmod +x "$HOME/.local/bin/"*

# PATH ortam değişkenini hem bash hem zsh için ekle
PATH_EXPORT='export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"'

for RC_FILE in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$RC_FILE" ]; then
        if ! grep -Fq "$PATH_EXPORT" "$RC_FILE"; then
            echo "$PATH_EXPORT" >> "$RC_FILE"
            echo "✓ Added PATH export to $RC_FILE"
        fi
    fi
done

# Geçerli oturum için de export et
export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"

echo ""
echo "========================================================================"
echo "🎉 AI AGENTS Multi-Agent Ekosistemi Başarıyla Kuruldu ve Hazır!"
echo "========================================================================"
echo "Terminalde herhangi bir klasörden doğrudan çalıştırabileceğiniz ajanlar:"
echo "  👑 ironman   -> Supreme Meta-Orchestrator (Tüm ekibi yöneten üst ajan)"
echo "  💻 cooker    -> Master Coding & Systems Agent (C/C++, ROS2, Python, Sıfır Hata)"
echo "  🎨 selimbey  -> Master UI/UX & Web Designer (Tailwind, Landing Page, Modern UI)"
echo "  ☕ sohbet    -> Personal Mentor, Chat & Life Coach (Feynman tekniği, samimi sohbet)"
echo "  🩺 doktor    -> Clinical Health & Biohack Specialist (Kanıta dayalı tıp, beslenme, spor)"
echo "  ✍️ murekkep  -> Master Writer & Paraphraser (Derin yeniden yazım, üslup dönüşümü)"
echo "  🤖 agent     -> Genel AI AGENTS CLI Başlatıcısı"
echo "========================================================================"
echo "💡 İpucu: Yeni bir terminal açarak veya 'source ~/.bashrc' diyerek hemen kullanabilirsiniz!"
