from flask import Flask, render_template, request, send_from_directory, send_file
import os, json, zipfile, datetime, time, io
location = os.path.expanduser("D:\\Фотографии\\")

class Cache(object):
    def __init__(self):
        self.new =          {}
        self.old =          {}
        self.to_delete =    {}
        self.to_view =      {}
        self.search =       {}
        self.tags =         {}
        self.active_tags =  []

    def clear(self):
        self.new =          {}
        self.old =          {}
        self.to_delete =    {}
        self.to_view =      {}
        self.search =       {}
        self.tags =         {}
        self.active_tags =  []

    def fill(self):
        try:
            f = open('data.json', 'r')
            self.old = json.loads(f.read())
            f.close()
            self.tags = {}
            for key in self.old:
                if self.old[key]:
                    for tag in self.old[key]:
                        if tag in self.tags:
                            self.tags[tag] += 1
                        else:
                            self.tags[tag] = 1
        except:
            print("No file")

    def dump(self):
        f = open('data.json', 'w')
        f.write(json.dumps(self.old, ensure_ascii=False, indent=2))
        f.close()

    def len(self):
        return {
            "new"       : len(self.new),
            "old"       : len(self.old),
            "to_delete" : len(self.to_delete),
            "to_view"   : len(self.to_view),
            "search"    : len(self.search)
        }

def search_tags(pattern, taglist):
    for tag in pattern:
        if not (tag in taglist):
            return False
    return True

def scan():
    cache.clear()
    wlk = os.walk(location)
    a = [os.path.join(dp, f)[len(location):] for dp, dn, fn in wlk for f in fn]
    for row in a:
        cache.new[row] = None
    cache.fill()

    for row in cache.old:
        if row in cache.new:
            del cache.new[row]
            if cache.old[row] is None:
                cache.to_view[row] = None
        else:
            cache.to_delete[row] = cache.old[row]

cache = Cache()
scan()
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная', cache=cache, len=cache.len())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/scan')
def scan_page():
    scan()
    return render_template('scan.html', title='Сканирование каталога', cache=cache, len=cache.len())

@app.route('/view')
def view():
    photo = request.args["photo"]
    return render_template('view.html', title='Просмотр фото', photo=photo, cache=cache, len=cache.len())

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        cache.search = {}
        l = [key for key in request.form]
        for ph in cache.old:
            if search_tags(l, cache.old[ph]):
                if not ph in cache.to_delete:
                    cache.search[ph] = cache.old[ph]
    return render_template('search.html', title='Найденные фото', cache=cache, len=cache.len())


@app.route('/apply', methods=['POST'])
def apply():
    photo = request.form["photo_id"]
    l = [key for key in request.form if key != 'photo_id']
    cache.active_tags = l
    if l:
        cache.old[photo] = l
        for tag in l:
            if tag in cache.tags:
                cache.tags[tag] += 1
            else:
                cache.tags[tag] = 1
        cache.dump()
        if photo in cache.to_view:
            del cache.to_view[photo]
        if photo in cache.new:
            del cache.new[photo]
    return next_page()

@app.route('/next')
def next_page():
    if "list" in request.args:
        lst = request.args["list"]
        if lst == "search":
            if cache.search:
                return render_template('view.html', title='Просмотр фото', photo=next(iter(cache.search)), cache=cache, len=cache.len())
    if cache.new:
        return render_template('view.html', title='Просмотр фото', photo=next(iter(cache.new)), cache=cache, len=cache.len())

@app.route('/tags')
def tags():
    return render_template('tags.html', title='Тэги', cache=cache, len=cache.len())


@app.route('/export')
def export():
    memory_file = io.BytesIO()
    zf = zipfile.ZipFile(memory_file, 'w')
    for file in cache.search:
        print(file)
        zf.write(file, arcname=file[file.rfind("\\")+1:])
    print(zf.filelist)
    zf.close()
    memory_file.seek(0)
    return send_file(io.BytesIO(memory_file.read()), attachment_filename=str(datetime.datetime.now()) + ".zip", as_attachment=True)

@app.route('/photo/<photo_id>')
def photo(photo_id):
    print(photo_id)
    return send_file(f"{location}\\{photo_id}")

@app.route('/arch')
def arch():
    return send_file("D:\\Share\\Сканер.zip",  as_attachment=True)

app.run(debug=True, host="0.0.0.0")