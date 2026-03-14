#!/usr/bin/env python3
"""🗄️ خزانتي الرقمية - Run Server"""

import uvicorn
from app.main import app
from app.database import init_db

if __name__ == "__main__":
    print("🚀 Starting خزانتي الرقمية...")
    print("📍 Open: http://localhost:8000")
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
