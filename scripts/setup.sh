#!/bin/bash

# NEXIS Platform - Quick Setup Script
# This script sets up both backend and frontend for development

set -e  # Exit on error

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "=================================="
echo "NEXIS Platform - Quick Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm found${NC}"

echo ""
echo "=================================="
echo "Setting up Backend"
echo "=================================="
echo ""

# Setup backend
cd "$PROJECT_ROOT/backend"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please review backend/.env and update if needed${NC}"
fi

# Train ML model
echo "🤖 Training ML model..."
python train_model.py

echo -e "${GREEN}✅ Backend setup complete!${NC}"

cd "$PROJECT_ROOT/frontend"

echo ""
echo "=================================="
echo "Setting up Frontend"
echo "=================================="
echo ""

# Install frontend dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

echo -e "${GREEN}✅ Frontend setup complete!${NC}"

echo ""
echo "=================================="
echo "🎉 Setup Complete!"
echo "=================================="
echo ""
echo "To start the platform:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   cd $PROJECT_ROOT/backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   cd $PROJECT_ROOT/frontend"
echo "   npm run dev"
echo ""
echo "3. Open browser:"
echo "   http://localhost:3000"
echo ""
echo "API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "=================================="
