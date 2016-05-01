""" JSON server """

import os

from json import dumps, load
from datetime import datetime


def json_format_template(path, user=None, url=None):
    with open(os.path.join(os.environ["WORKDIR"], "templates", path)) as temp:
        return json_format_data(load(temp), user, url)
    return None


def json_format_data(main, user=None, url=None):
    if not isinstance(main, dict):
        return None

    assert len(main) == 1
    key, val = main.popitem()
    meta = {
        "version": 1,
        "generated": datetime.now().isoformat(),
        "name": key
    }

    if user:
        meta["username"] = user.get_username()
    if url:
        meta["url"] = url

    data = {"meta": meta, "data": val}  # Dictionary.format(val)}
    return dumps(data, indent=2).encode("UTF-8")

