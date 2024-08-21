from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, GET!")

class Server:
    def __init__(self, host='localhost', port=8000):
        self.host = 'localhost'
        self.port = 8000

    def __run_server(self, httpd):
        print("Server starting...")
        httpd.serve_forever()

    def __stop_server_after_duration(self, httpd: HTTPServer, duration):
        time.sleep(duration)
        print(f"Stopping server after {duration} seconds")
        httpd.shutdown()

    def run(self, server_class=HTTPServer, handler_class=GameHandler, duration=30):
        server_address = (self.host, self.port)
        httpd = server_class(server_address, handler_class)
        server_thread = threading.Thread(target=self.__run_server, args=(httpd,))
        server_thread.start()

        stop_timer_thread = threading.Thread(target=self.__stop_server_after_duration, args=(httpd, duration))
        stop_timer_thread.start()

        for i in range(1,4):
            time.sleep(10)
            print(i*10)

        server_thread.join()
        print("Server thread has finished.")