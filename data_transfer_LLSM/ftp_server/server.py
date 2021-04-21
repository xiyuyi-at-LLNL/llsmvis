from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import yaml
import os

def read_config():
    config_path = os.path.join(os.getcwd(), "config.yaml")
    print(config_path)
    with open(config_path, "r") as f: 
        return yaml.safe_load(f)

def main():
    config_ftp = read_config().get("FTP")
    
    PORT = config_ftp.get("PORT")
    IP = config_ftp.get("IP")
    FTP_USER = config_ftp.get("FTP_USER")
    FTP_PASSWORD = config_ftp.get("FTP_PASSWORD")
    SERVERNAME=config_ftp.get("SERVERNAME")
    FTP_DIRECTORY = config_ftp.get("FTP_DIRECTORY")

    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = SERVERNAME

    address = (IP, PORT)
    server = FTPServer(address, handler)

    server.max_cons = 1
    server.max_cons_per_ip = 1

    server.serve_forever()

if __name__ == '__main__':
    main()