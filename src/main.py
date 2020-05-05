import uvicorn
from application import mp_backend

if __name__ == '__main__':
    uvicorn.run(mp_backend.mpApi, host="0.0.0.0", port=8000)
