import uvicorn
from flow_guardian_x.api.server import app
from flow_guardian_x.config import API_HOST, API_PORT

def main():
    print("--- Flow Guardian X - Starting System ---")
    print(f"Server starting at http://{API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    main()
