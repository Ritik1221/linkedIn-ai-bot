#!/bin/bash
# LinkedIn AI Agent Deployment Script
# This script sets up the LinkedIn AI Agent backend on a server
#
# Note: Before running this script on Linux, make it executable with:
#   chmod +x deploy.sh

set -e

# Configuration
INSTALL_DIR="/opt/linkedin-agent-backend"
CONFIG_DIR="/etc/linkedin-agent"
CELERY_USER="celery"
VENV_DIR="$INSTALL_DIR/venv"
REPO_URL="https://github.com/yourusername/linkedin-agent-backend.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}LinkedIn AI Agent Deployment Script${NC}"
echo -e "${YELLOW}This script will install the LinkedIn AI Agent backend on your server.${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Function to display step information
step() {
    echo -e "${GREEN}==> $1${NC}"
}

# Install system dependencies
step "Installing system dependencies"
apt-get update
apt-get install -y python3 python3-venv python3-pip postgresql postgresql-contrib redis-server supervisor nginx git

# Create celery user if it doesn't exist
step "Creating celery user"
if ! id "$CELERY_USER" &>/dev/null; then
    useradd -r -s /bin/false "$CELERY_USER"
    echo -e "${GREEN}Created $CELERY_USER user${NC}"
else
    echo -e "${YELLOW}User $CELERY_USER already exists${NC}"
fi

# Create installation and configuration directories
step "Creating directories"
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"

# Clone the repository
step "Cloning repository"
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "${YELLOW}Git repository already exists. Pulling latest changes...${NC}"
    cd "$INSTALL_DIR"
    git pull
else
    echo -e "${GREEN}Cloning fresh repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Set up virtual environment
step "Setting up virtual environment"
cd "$INSTALL_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file if it doesn't exist
step "Setting up environment configuration"
if [ ! -f "$CONFIG_DIR/celery.env" ]; then
    cp "$INSTALL_DIR/scripts/celery.env.sample" "$CONFIG_DIR/celery.env"
    echo -e "${YELLOW}Please edit $CONFIG_DIR/celery.env with your configuration${NC}"
    echo -e "${YELLOW}Press Enter to continue when done...${NC}"
    read
else
    echo -e "${YELLOW}Environment file already exists at $CONFIG_DIR/celery.env${NC}"
fi

# Fix permissions
step "Setting permissions"
chown -R "$CELERY_USER:$CELERY_USER" "$INSTALL_DIR"
chown -R "$CELERY_USER:$CELERY_USER" "$CONFIG_DIR"
chmod 600 "$CONFIG_DIR/celery.env"

# Copy systemd service files
step "Installing systemd service files"
cp "$INSTALL_DIR/scripts/celery-worker.service" /etc/systemd/system/
cp "$INSTALL_DIR/scripts/celery-beat.service" /etc/systemd/system/
cp "$INSTALL_DIR/scripts/celery-api.service" /etc/systemd/system/
systemctl daemon-reload

# Set up database
step "Setting up database"
echo -e "${YELLOW}Please enter PostgreSQL password for postgres user:${NC}"
read -s PGPASSWORD
export PGPASSWORD

# Check if database already exists
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw linkedin_agent; then
    echo -e "${YELLOW}Database linkedin_agent already exists${NC}"
else
    echo -e "${GREEN}Creating database...${NC}"
    sudo -u postgres psql -c "CREATE DATABASE linkedin_agent;"
    echo -e "${GREEN}Database created successfully${NC}"
fi

# Run database migrations
step "Running database migrations"
source "$CONFIG_DIR/celery.env"
cd "$INSTALL_DIR"
source "$VENV_DIR/bin/activate"
alembic upgrade head

# Start services
step "Starting services"
systemctl start celery-worker.service
systemctl start celery-beat.service
systemctl start celery-api.service
systemctl enable celery-worker.service
systemctl enable celery-beat.service
systemctl enable celery-api.service

# Check service status
step "Checking service status"
systemctl status celery-worker.service --no-pager
systemctl status celery-beat.service --no-pager
systemctl status celery-api.service --no-pager

echo ""
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Worker API is available at: http://localhost:8001${NC}"
echo -e "${YELLOW}Health check: http://localhost:8001/health${NC}"
echo -e "${YELLOW}Metrics: http://localhost:8001/metrics${NC}"
echo ""
echo -e "${YELLOW}Remember to set up your API service separately.${NC}"
echo -e "${YELLOW}Refer to the README.md for more information.${NC}" 