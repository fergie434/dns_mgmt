import os
import tdnss
from dotenv import load_dotenv

load_dotenv()

tdns_api_key=os.getenv('tdns_api_key')
fortigate_api_key=os.getenv('fortigate_api_key')

def main():
    ...

if __name__ == '__main__':
    main()
