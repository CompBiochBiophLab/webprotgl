""" Parses POST arguments """

from urllib.parse import unquote_plus

def parse(env = None, data = None):
  """Parses simple POST arguments, format key=val&key2=val2&..."""
  if env:
    length = env["CONTENT_LENGTH"]
    if not length:
      return None
    data = env["wsgi.input"].read(int(length)).decode("UTF-8")
  args = dict()
  while True:
    key_sep = data.find("=")
    val_sep = data.find("&", key_sep)
    if key_sep < 0:
      break
    
    key = data[0:key_sep]
    if val_sep < 0:
      args[key] = unquote_plus(data[key_sep+1:])
      break
    val = unquote_plus(data[key_sep+1:val_sep])
    args[key] = val
    data = data[val_sep+1:]
  return args
  



#            data = BytesIO()
#            stream = self.__env["wsgi.input"]
#            while length > 0:
#              part = stream.read(min(length, 1024*200))
#              if not part:
#                break
#              data.write(part)
#              length -= len(part)
#            data.seek(0)
#            paper = self.__db.save_paper(self.__author, data.getvalue())
#            if not paper:
#              status = 415

