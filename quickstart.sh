#!/bin/bash
# Quick Start Script for SEO Optimizer SaaS

set -e

echo "🚀 SEO Optimizer SaaS - Quick Start"
echo "===================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/7]${NC} Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo -e "${BLUE}[2/7]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install dependencies
echo -e "${BLUE}[3/7]${NC} Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencies installed"

# Download NLTK data
echo -e "${BLUE}[4/7]${NC} Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} NLTK data downloaded"

# Run migrations
echo -e "${BLUE}[5/7]${NC} Running database migrations..."
cd seo_saas
python manage.py migrate > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Database migrations completed"

# Collect static files
echo -e "${BLUE}[6/7]${NC} Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Static files collected"

# Create superuser option
echo -e "${BLUE}[7/7]${NC} Django Setup"
echo "Do you want to create a superuser for admin access? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser
fi

echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "2. Open your browser:"
echo "   http://localhost:8000"
echo ""
echo "3. Access admin panel:"
echo "   http://localhost:8000/admin"
echo ""
echo "4. Read the guides:"
echo "   - SEO Guide: http://localhost:8000/guide"
echo "   - Setup Guide: ../SAAS_SETUP_GUIDE.md"
echo ""
echo -e "${BLUE}Happy analyzing! 🎉${NC}"
