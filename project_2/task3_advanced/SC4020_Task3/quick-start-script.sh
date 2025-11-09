#!/bin/bash

# Health Assistant - Quick Setup Script
# This script automates the setup process

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup
main() {
    clear
    print_header "HEALTH ASSISTANT - AUTOMATED SETUP"
    echo ""
    
    # Check prerequisites
    print_info "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"
    
    if ! command_exists pip3; then
        print_error "pip3 is not installed. Please install pip."
        exit 1
    fi
    print_success "pip3 found"
    
    echo ""
    print_header "STEP 1: SETTING UP PYTHON ENVIRONMENT"
    
    # Create virtual environment (optional but recommended)
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate || . venv/Scripts/activate
    print_success "Virtual environment activated"
    
    echo ""
    print_header "STEP 2: INSTALLING DEPENDENCIES"
    
    print_info "Installing Python packages..."
    pip install -r requirements.txt --quiet
    print_success "Python dependencies installed"
    
    echo ""
    print_header "STEP 3: CREATING DIRECTORY STRUCTURE"
    
    if [ ! -d "models" ]; then
        mkdir models
        print_success "Created models directory"
    else
        print_info "Models directory already exists"
    fi
    
    echo ""
    print_header "STEP 4: TRAINING ML MODELS"
    
    print_info "This may take a few minutes..."
    python train_models.py
    print_success "Models trained successfully"
    
    echo ""
    print_header "STEP 5: TESTING API SERVER"
    
    print_info "Starting Flask server in background..."
    python app.py &
    SERVER_PID=$!
    
    sleep 5
    
    print_info "Testing API health..."
    if curl -s http://localhost:5000/api/health > /dev/null; then
        print_success "API server is running!"
    else
        print_error "API server failed to start"
        kill $SERVER_PID 2>/dev/null
        exit 1
    fi
    
    # Stop test server
    kill $SERVER_PID 2>/dev/null
    
    echo ""
    print_header "SETUP COMPLETE!"
    echo ""
    print_success "All components installed successfully!"
    echo ""
    echo -e "${YELLOW}To start the application:${NC}"
    echo ""
    echo -e "  ${GREEN}1. Start Backend:${NC}"
    echo -e "     source venv/bin/activate  # or: . venv/Scripts/activate (Windows)"
    echo -e "     python app.py"
    echo ""
    echo -e "  ${GREEN}2. Start Frontend (in new terminal):${NC}"
    echo -e "     cd frontend"
    echo -e "     npm install"
    echo -e "     npm start"
    echo ""
    echo -e "${YELLOW}Or use Docker:${NC}"
    echo -e "     docker-compose up --build"
    echo ""
    echo -e "${YELLOW}Test the API:${NC}"
    echo -e "     python test_api.py"
    echo ""
    print_header "ENJOY YOUR HEALTH ASSISTANT!"
}

# Run main function
main
