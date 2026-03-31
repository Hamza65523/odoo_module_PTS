"""Standalone script to start the PTS backend. Copy to server and run:
   python run_server.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
