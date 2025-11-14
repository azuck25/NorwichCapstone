# main.py

from database import initialize_database,Base,engine  # Optional: one-time DB setup
from pyngrok import ngrok
import uvicorn, subprocess

ngrok.set_auth_token("2aPOIu0sWqUH5ijSYf5xr2NFTzD_4Rmhn8BNNkpD4CzGCePGG")

def main():
    #First, we initialize the database, mapping the classes to the database schema
    print("Initializing database...")
    initialize_database()
    # Start a ngrok tunnel to the local FastAPI app
    public_url = ngrok.connect(8000,proto="http",domain="ingestsymbol.ngrok.pro")
    # Run FastAPI app from data_injest.py
    print(f"App is live at: {public_url}")
    uvicorn.run("db_commit:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
