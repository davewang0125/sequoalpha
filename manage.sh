#!/bin/bash

# Service Management Script for SequoAlpha
# Usage: ./manage.sh [start|stop|restart|status|logs]

SERVICE_NAME="sequoalpha"

case "$1" in
    start)
        echo "🚀 Starting SequoAlpha..."
        sudo systemctl start $SERVICE_NAME
        sudo systemctl start nginx
        echo "✅ Services started"
        ;;
    stop)
        echo "🛑 Stopping SequoAlpha..."
        sudo systemctl stop $SERVICE_NAME
        echo "✅ Service stopped"
        ;;
    restart)
        echo "🔄 Restarting SequoAlpha..."
        sudo systemctl restart $SERVICE_NAME
        sudo systemctl restart nginx
        echo "✅ Services restarted"
        ;;
    status)
        echo "📊 SequoAlpha Backend Status:"
        sudo systemctl status $SERVICE_NAME --no-pager -l
        echo ""
        echo "📊 Nginx Status:"
        sudo systemctl status nginx --no-pager -l
        ;;
    logs)
        echo "📋 Following SequoAlpha logs (Ctrl+C to exit)..."
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    errors)
        echo "❌ Recent errors (last 50 lines):"
        sudo journalctl -u $SERVICE_NAME -n 50 -p err
        ;;
    test)
        echo "🧪 Testing backend API..."
        curl -s http://localhost:8000/ | python3 -m json.tool || echo "Backend not responding"
        echo ""
        echo "🧪 Testing nginx..."
        curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost/
        ;;
    backup)
        echo "💾 Creating database backup..."
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        sudo -u postgres pg_dump sequoalpha > $BACKUP_FILE
        echo "✅ Backup created: $BACKUP_FILE"
        ;;
    *)
        echo "SequoAlpha Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|errors|test|backup}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the backend service and nginx"
        echo "  stop     - Stop the backend service"
        echo "  restart  - Restart backend and nginx"
        echo "  status   - Show service status"
        echo "  logs     - Follow service logs (live)"
        echo "  errors   - Show recent errors"
        echo "  test     - Test if services are responding"
        echo "  backup   - Create database backup"
        echo ""
        exit 1
        ;;
esac

exit 0
