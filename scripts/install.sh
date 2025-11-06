#!/usr/bin/env bash
# diane, one-line installer
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash
#   # or
#   wget -qO- https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║         diane, installer               ║"
echo "║  Frictionless thought capture CLI      ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Found Python ${python_version}${NC}"

# Install diane
echo -e "${YELLOW}Installing diane, ...${NC}"
pip3 install --user diane-cli 2>&1 | grep -v "WARNING" || true

# Or if installing from local directory
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    echo -e "${YELLOW}Installing from local directory...${NC}"
    pip3 install --user -e ".[all]"
fi

# Check if diane is in PATH
if ! command -v diane &> /dev/null; then
    echo -e "${YELLOW}⚠️  diane not in PATH. Adding to shell config...${NC}"

    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        shell_config="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_config="$HOME/.zshrc"
    else
        shell_config="$HOME/.profile"
    fi

    # Add to PATH
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_config"
    export PATH="$HOME/.local/bin:$PATH"
    echo -e "${GREEN}✓ Added to PATH in ${shell_config}${NC}"
fi

# Setup shell completions
echo -e "${YELLOW}Installing shell completions...${NC}"

# Bash
if [ -n "$BASH_VERSION" ]; then
    mkdir -p ~/.bash_completion.d
    if [ -f "scripts/completions/diane.bash-completion" ]; then
        cp scripts/completions/diane.bash-completion ~/.bash_completion.d/diane
        echo "source ~/.bash_completion.d/diane" >> ~/.bashrc
        echo -e "${GREEN}✓ Bash completions installed${NC}"
    fi
fi

# Zsh
if [ -n "$ZSH_VERSION" ]; then
    mkdir -p ~/.zsh/completion
    if [ -f "scripts/completions/diane.zsh-completion" ]; then
        cp scripts/completions/diane.zsh-completion ~/.zsh/completion/_diane
        echo "fpath=(~/.zsh/completion \$fpath)" >> ~/.zshrc
        echo "autoload -Uz compinit && compinit" >> ~/.zshrc
        echo -e "${GREEN}✓ Zsh completions installed${NC}"
    fi
fi

# Install quick capture shortcuts
if [ -f "scripts/quick-capture.sh" ]; then
    mkdir -p ~/.diane
    cp scripts/quick-capture.sh ~/.diane/

    # Add to shell config
    if [ -n "$BASH_VERSION" ]; then
        echo "source ~/.diane/quick-capture.sh" >> ~/.bashrc
    elif [ -n "$ZSH_VERSION" ]; then
        echo "source ~/.diane/quick-capture.sh" >> ~/.zshrc
    fi

    echo -e "${GREEN}✓ Quick capture shortcuts installed${NC}"
fi

# Test installation
echo -e "${YELLOW}Testing installation...${NC}"
if diane, --help &> /dev/null; then
    echo -e "${GREEN}✓ diane, is working!${NC}"
else
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

# Print success message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✅ Installation complete!          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Quick start:${NC}"
echo "  echo 'My first thought' | diane,"
echo "  diane, --list"
echo "  diane, --stats"
echo ""
echo -e "${BLUE}Ultra-fast shortcuts:${NC}"
echo "  d 'quick note'      # fastest capture"
echo "  dc                  # capture clipboard"
echo "  dt work 'meeting'   # capture with tag"
echo "  dl                  # list records"
echo "  dst                 # show stats"
echo ""
echo -e "${YELLOW}⚡ Reload your shell to activate shortcuts:${NC}"
echo "  source ~/.bashrc    # or ~/.zshrc"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  README.md, FEATURES.md, INSTALL.md"
echo ""
echo -e "${GREEN}Happy capturing! 🎉${NC}"
