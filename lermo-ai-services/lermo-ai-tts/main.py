import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

# host=os.getenv('HOST')
# port=os.getenv('PORT')
# app_name=os.getenv('APP_NAME')

host='0.0.0.0'
port=8081
app_name=os.getenv('APP_NAME')

if __name__ == '__main__':
    uvicorn.run(app_name, host=host, port=port)