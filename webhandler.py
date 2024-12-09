import re, socket, ssl, time
from constants import *

class WebHandler():

    def __init__(self):
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_cert_chain(CERT_PATH,KEY_PATH)

        self.maze_pattern = re.compile("`{3}A maze with a mouse in the middle(.*)`{3}", re.S)
        self.cleaner_dict = {96:32, 44:32, 128000:83, 128001:83}

    def send_request(self, request : str):
        server_socket = socket.create_connection(("alchemi.dev",1965))
        server_socket = self.ssl_context.wrap_socket(server_socket, server_hostname = "alchemi.dev")
        server_socket.sendall(request)
        buffer_data = server_socket.makefile("r", encoding="UTF-8")
        page_data = buffer_data.read()
        buffer_data.close()
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
        return page_data

    def request_page(self):
        return self.send_request(("gemini://alchemi.dev/maze/app\r\n").encode("UTF-8"))

    def request_movement(self, direction : str):
        return self.extract_maze(self.send_request(("gemini://alchemi.dev/maze/app?"+direction+"\r\n").encode("UTF-8")))

    def extract_maze(self, page_string):
        maze_string = self.maze_pattern.search(page_string).group(0)
        maze_string = maze_string.replace("```A maze with a mouse in the middle","").replace("```","")
        maze_string = maze_string.strip()
        
        maze_string = maze_string.translate(self.cleaner_dict)
        maze_string = maze_string.replace("S","  ").replace("\n","")
        
        return maze_string

    def get_maze(self):
        return self.extract_maze(self.request_page())