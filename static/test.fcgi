from fcgi import WSGIServer

def myapp(environ, start_response):
  print("Got request: %s"%environ)
  start_response("200 OK", [("Content-Type", "text/plain")])
  return ["Hello World!\n"]

WSGIServer(myapp, bindAddress="/tmp/fcgi.sock").run()
