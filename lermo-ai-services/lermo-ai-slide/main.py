import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

host='0.0.0.0'
port=8082
app_name="app.main:app"

if __name__ == '__main__':
    uvicorn.run(app_name, host=host, port=port)