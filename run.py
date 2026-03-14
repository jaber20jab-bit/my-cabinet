#!/usr/bin/env python3
"""🗄️ خزانتي الرقمية - Run Server"""

import os
import uvicorn
from app.main import app
from app.database import init_db

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting خزانتي الرقمية...")
    print(f"📍 Open: http://localhost:{port}")
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=port)
