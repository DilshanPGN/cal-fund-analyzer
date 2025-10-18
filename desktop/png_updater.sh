#!/bin/bash
# CAL Fund PNG Updater - Unix/Linux/Mac Shell Script
# This script provides easy access to PNG updater functionality

echo "CAL Fund PNG Updater"
echo "===================="

case "$1" in
    "help")
        echo "Usage: ./png_updater.sh [command]"
        echo ""
        echo "Commands:"
        echo "  help     - Show this help message"
        echo "  status   - Show status of CSV and PNG files"
        echo "  monitor  - Monitor CSV files and auto-update PNGs"
        echo "  update   - Update PNG files for all CSV files (default)"
        echo ""
        echo "Examples:"
        echo "  ./png_updater.sh           # Update all files"
        echo "  ./png_updater.sh status    # Show file status"
        echo "  ./png_updater.sh monitor   # Start monitoring"
        ;;
    "status")
        python3 png_updater.py --status
        ;;
    "monitor")
        python3 png_updater.py --monitor
        ;;
    "update"|"")
        python3 png_updater.py --all
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use 'help' to see available commands"
        exit 1
        ;;
esac
