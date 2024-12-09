import re, socket, ssl
from constants import *

class WebHandler():

    def __init__(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.load_cert_chain(CERT_PATH,KEY_PATH)
        
        self.server_socket = socket.create_connection(("alchemi.dev",1965))
        self.server_socket = ssl_context.wrap_socket(self.server_socket, server_hostname = "alchemi.dev")
        
        self.maze_pattern = re.compile("`{3}A maze with a mouse in the middle(.*)`{3}", re.S)
        self.cleaner_dict = {96:32, 44:32, 128000:83, 128001:83}


    def request_page(self):
        self.server_socket.sendall(("gemini://alchemi.dev/maze/app\r\n").encode("UTF-8"))
       # socket keep response in an internal buffer, we access it like a file
        buffer_data = self.server_socket.makefile("r", encoding="UTF-8")
        page_data = buffer_data.read()
        buffer_data.close()

        return page_data

    def request_movement(self, direction : str):
        self.server_socket.sendall(("gemini://alchemi.dev/maze/app?r\r\n").encode("UTF-8"))
       # Directions can be 'l', 'd', 'u', 'r' for left, down, up, right
        buffer_data = self.server_socket.makefile("r", encoding="UTF-8")
        page_data = buffer_data.read()
        buffer_data.close()

        return page_data

    def extract_maze(self, page_string):
        maze_string = self.maze_pattern.search(page_string).group(0)
        maze_string = maze_string.replace("```A maze with a mouse in the middle","").replace("```","")
        maze_string = maze_string.strip()
        
        maze_string = maze_string.translate(self.cleaner_dict)
        maze_string = maze_string.replace("S","  ").replace("\n","")
        
        return maze_string

    def get_maze(self):
        return self.extract_maze(self.request_page())