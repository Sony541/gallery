from config import active_config
import json


def get_old():
    try:
        f = open(active_config['data_file'], 'rb')
        ret = json.loads(f.read().decode('utf8'))
        f.close()
        return ret
    except:
        print("No file")
        return False


def write(ob, name):
    if name:
        return _write_one(ob, name)
    else:
        return _write_all(ob)


def _write_one(ob, name):
    _write_all(ob)


def _write_all(ob):
    f = open(active_config['data_file'], 'wb')
    f.write(json.dumps(ob, ensure_ascii=False, indent=2).encode('utf8'))
    f.close()
