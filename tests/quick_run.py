import re


p = re.compile(".*")
p.ma

def _get_key(path, routes:{}):
    for pattern, key_template in routes.items():
        match = pattern.match(path)
        if match:
            return match.expand(key_template)
    return None

if __name__ == "__main__":
    PATH = "/api/soundcloud/478324982"

    ROUTES = {
        "/api/([a-zA-Z0-9-_]+)/([0-9]+)+": r"API-\1-\2",
        ".*": "ERROR"
    }

    key = _get_key(PATH, ROUTES)
    print(key)