""" Parses POST arguments """

from io import BytesIO
import logging
from urllib.parse import unquote_plus


def parse(env=None, data=None):
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


def parse_binary(env, max=50*1024*1024):
    """Parses binary POSTed data (files, ...), with a maximum accepted length"""
    length = int(env["CONTENT_LENGTH"])
    if length > max:
        logging.error(str(length) + " > max length")
        return 413
    data = BytesIO()
    stream = env["wsgi.input"]
    while length > 0:
        part = stream.read(min(length, 1024*200))
        if not part:
            break
        data.write(part)
        length -= len(part)
    data.seek(0)

    # Parse information
    lines = data.read().split(b'\r\n')
    delimiter = lines[0]
    in_data = False
    file = dict()
    for line in lines[1:]:
        if line == b'':
            #if in_data:
            #    break
            #else:
            in_data = True
        elif in_data:
            file["data"] = line
            break
        else:
            if line.startswith(b'Content-Disposition'):
                sub = line.split(b';')
                for item in sub[1:]:
                    if item.startswith(b' name'):
                        file["id"] = item[7:-1].decode("UTF-8")
                    elif item.startswith(b' filename'):
                        file["name"] = item[11:-1].decode("UTF-8")
            elif line.startswith(b'Content-Type'):
                file["content_type"] = line.split(b' ')[1].decode("UTF-8")
    return file