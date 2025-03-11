
import uvicorn
from api.service import app

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=80) # Production: this is for docker deployment 
    uvicorn.run(app, host="127.0.0.1", port=8000) # Development: this is for local development
    
# uvicorn main:app --reload
