#!/bin/bash
# AI Lab - Complete Command Reference
# This script displays all available commands and their usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "\n${BLUE}══════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════${NC}\n"
}

print_section() {
    echo -e "\n${GREEN}▸ $1${NC}"
}

print_command() {
    echo -e "  ${YELLOW}→${NC} $1"
}

print_info() {
    echo -e "  ${CYAN}ℹ${NC} $1"
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

# Main header
print_header "AI Lab — Command Reference"

# Section 1: Setup Commands
# print_section "📦 INITIAL SETUP (First Time Only)"
# print_command "python3 -m venv venv"
# echo "       Create virtual environment"
# print_command "source venv/bin/activate"
# echo "       Activate virtual environment"
# print_command "pip install -r requirements.txt"
# echo "       Install all dependencies"
# print_command "cp .env .env.local"
# echo "       Copy environment configuration"
# print_command "python manage.py migrate"
# echo "       Create database tables"
# print_command "python manage.py createsuperuser"
# echo "       Create admin user (skip if using default: admin@ailab.com / admin123)"

# Section 2: Data Seeding Commands
print_section "🌱 DATA SEEDING (Run in order)"
print_command "python manage.py seed_data"
echo "       Seed 7 core AI modules (AI Basics, ML, Deep Learning, GenAI, LLM Systems, Agentic AI, Playground)"
print_command "python manage.py seed_foundation"
echo "       Seed 6 foundation modules for Class 8-10 (Binary, Data, Programming, Math, Building Models, Real World AI)"
print_command "python manage.py seed_python_class7"
echo "       Seed Class 7 Python course (variables, loops, functions, projects)"
print_command "python manage.py seed_glossary"
echo "       Seed 30+ glossary terms and 5 learning paths (Class 8-12)"
print_command "python manage.py seed_resources"
echo "       Seed curated learning resources (videos, courses, books) for all modules"
print_command "python manage.py seed_badges"
echo "       Seed 13 gamification badges (achievements, streaks, rewards)"

# # Section 3: Utility Commands
# print_section "🔧 UTILITY COMMANDS"
# print_command "python manage.py index_codebase"
# echo "       Index codebase for AI-powered code exploration (jCodeMunch)"
# print_command "python manage.py index_codebase --force"
# echo "       Force re-index the codebase"
# print_command "python manage.py generate_daily_challenge"
# echo "       Generate today's daily challenge"
# print_command "python manage.py generate_daily_challenge --date 2025-06-01"
# echo "       Generate challenge for a specific date"
# print_command "python manage.py send_weekly_report"
# echo "       Send weekly progress emails to students and teachers"

# # Section 4: Server Commands
# print_section "🚀 STARTING THE SERVER"
# print_command "./start.sh"
# echo "       Start server with auto-migration and seeding (recommended)"
# print_command "daphne -b 0.0.0.0 -p 8000 ailab.asgi:application"
# echo "       Start Daphne ASGI server manually (WebSocket support)"
# print_command "python manage.py runserver"
# echo "       Start Django development server (no WebSocket support)"

# # Section 5: Build & Deploy
# print_section "🏗️ BUILD & DEPLOYMENT"
# print_command "./build.sh"
# echo "       Build for production (install deps, collectstatic, migrate)"
# print_command "python manage.py collectstatic --noinput"
# echo "       Collect static files for production"
# print_command "python manage.py migrate --run-syncdb"
# echo "       Run migrations and create tables if they don't exist"

# # Section 6: Quick Start Sequences
# print_section "⚡ QUICK START SEQUENCES"

# echo -e "\n${YELLOW}Option A: Full Setup (Recommended for first time)${NC}"
# print_command "source venv/bin/activate"
# print_command "python manage.py migrate"
# print_command "python manage.py seed_data"
# print_command "python manage.py seed_foundation"
# print_command "python manage.py seed_glossary"
# print_command "python manage.py seed_badges"
# print_command "python manage.py collectstatic --noinput"
# print_command "./start.sh"

# echo -e "\n${YELLOW}Option B: Minimal Setup (Quick start)${NC}"
# print_command "python manage.py migrate"
# print_command "python manage.py seed_data"
# print_command "./start.sh"

# echo -e "\n${YELLOW}Option C: Complete Setup (All content)${NC}"
# print_command "python manage.py migrate"
# print_command "python manage.py seed_data"
# print_command "python manage.py seed_foundation"
# print_command "python manage.py seed_python_class7"
# print_command "python manage.py seed_glossary"
# print_command "python manage.py seed_resources"
# print_command "python manage.py seed_badges"
# print_command "python manage.py index_codebase"
# print_command "python manage.py collectstatic --noinput"
# print_command "./start.sh"

# # Section 7: Command Locations
# print_section "📁 COMMAND FILE LOCATIONS"
# echo -e "  ${CYAN}modules/management/commands/${NC}"
# echo "    - seed_data.py          → Core AI modules"
# echo "    - seed_foundation.py    → Foundation modules (8-10)"
# echo "    - seed_python_class7.py → Python for Class 7"
# echo "    - seed_glossary.py      → Glossary & learning paths"
# echo "    - seed_resources.py     → External learning resources"
# echo -e "\n  ${CYAN}gamification/management/commands/${NC}"
# echo "    - seed_badges.py        → Gamification badges"
# echo -e "\n  ${CYAN}ai_service/management/commands/${NC}"
# echo "    - index_codebase.py     → Code indexing"
# echo -e "\n  ${CYAN}school/management/commands/${NC}"
# echo "    - generate_daily_challenge.py → Daily challenges"
# echo "    - send_weekly_report.py       → Weekly reports"

# # Section 8: Key Information
# print_section "🔑 KEY INFORMATION"
# print_info "Admin Panel:     http://localhost:8000/admin/"
# print_info "Default Admin:   admin@ailab.com / admin123"
# print_info "WebSocket URL:   ws://localhost:8000/ws/ai/chat/"
# print_info "Database:        ailab_db.sqlite3 (local)"
# print_info "Server Port:     8000"
# print_info "ASGI Server:     Daphne (supports WebSockets)"

# # Section 9: Troubleshooting
# print_section "🔧 TROUBLESHOOTING"
# print_command "python manage.py check"
# echo "       Check for configuration issues"
# print_command "python manage.py migrate --run-syncdb"
# echo "       Fix missing database tables"
# print_command "python manage.py collectstatic --clear"
# echo "       Clear and rebuild static files"
# print_command "pip install -r requirements.txt --upgrade"
# echo "       Upgrade all dependencies"

# # Footer
# echo -e "\n${BLUE}══════════════════════════════════════════${NC}"
# echo -e "${GREEN}  For more info, see README.md${NC}"
# echo -e "${BLUE}══════════════════════════════════════════${NC}\n"