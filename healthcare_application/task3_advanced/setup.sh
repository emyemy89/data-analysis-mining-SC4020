#!/bin/bash

# Health Assistant Setup Script
# Automated setup for development environment

set -e

echo "============================================"
echo "  Health Assistant - Automated Setup"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}[1/7] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found $PYTHON_VERSION${NC}"

# Check Node.js (optional for frontend)
echo -e "${YELLOW}[2/7] Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found (optional, needed for frontend)${NC}"
fi

# Create virtual environment
echo -e "${YELLOW}[3/7] Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}[4/7] Activating virtual environment...${NC}"
source venv/bin/activate || source venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
echo -e "${YELLOW}[5/7] Installing Python dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Create models directory
echo -e "${YELLOW}[6/7] Creating models directory...${NC}"
mkdir -p models
echo -e "${GREEN}✓ Models directory created${NC}"

# Train models
echo -e "${YELLOW}[7/7] Training machine learning models...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
python train-models-script.py
echo -e "${GREEN}✓ Models trained successfully${NC}"

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Setup Complete! 🎉${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "To start the backend server:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate  (Linux/Mac)"
echo "     venv\\Scripts\\activate  (Windows)"
echo "  2. Run: python app.py"
echo ""
echo "To start the frontend (optional):"
echo "  1. cd frontend"
echo "  2. npm install"
echo "  3. npm start"
echo ""
echo "Or use Docker:"
echo "  docker-compose up --build"
echo ""
