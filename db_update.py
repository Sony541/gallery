from config import active_config
import json


def get_old():
    try:
        f = open(active_config['data_file'], 'r')
        ret = json.loads(f.read())
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
    f = open(active_config['data_file'], 'w')
    f.write(json.dumps(ob, ensure_ascii=False, indent=2))
    f.close()
