# coding=utf-8
from flask import Flask, render_template, request, send_from_directory, send_file, redirect, url_for, abort
import os, json, zipfile, datetime, time, io
from scanner import Cache
from config import active_config

cache = Cache()
cache.scan()

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Главная', cache=cache.memory,
                           len=cache.len(), dir=active_config['location'])

@app.route('/problems')
def problems():
    return render_template('problems.html', title='Разрешение конфликтов', cache=cache.memory, len=cache.len())


@app.route('/problems_resolve', methods=['POST'])
def problems_resolve():
    f = request.form.to_dict(flat=False)
    cache.resolve_problems(f)
    return render_template('problems_resolve.html', title='Разрешение конфликтов', cache=cache.memory, len=cache.len(), form=f)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/scan/')
def scan():
    cache.scan()
    return render_template('scan.html', title='Сканирование каталога', cache=cache.memory, len=cache.len())

@app.route('/photo')
def photo():
    photo_id = request.args.get('photo_id')
    path = "%s%s" % (active_config['location'], photo_id)
    print(path)
    return send_file(path)


@app.route('/view')
def view():
    folder = request.args.get('folder')
    photo_id = request.args.get('photo_id')
    if not (folder and photo_id):
        folder = "to_view"
        if folder in cache.memory:
            if cache.memory[folder]:
                photo_id = cache.memory[folder][0]
            else:
                abort(404, "Нет фотографий для просмотра")
        else:
            abort(404, "Нет фотографий для просмотра")
        return redirect(url_for('view', photo_id=photo_id, folder=folder))

    return render_template('view.html', title='Просмотр фото', photo=photo_id,
                           folder=folder, cache=cache.memory, len=cache.len())


@app.route('/apply', methods=['POST'])
def apply():
    photo = request.form["photo_id"]
    l = [key for key in request.form if key != 'photo_id']
    cache.active_tags = l
    if l:
        if 'new' in cache.memory:
            if photo in cache.memory['new']:
                cache.memory['old'][photo] = cache.memory['new'][photo]
        cache.memory['old'][photo]['tags'] = l
        if 'tags' not in cache.memory:
            cache.memory['tags'] = {key : 1 for key in l}
        else:
            for tag in l:
                if tag in cache.memory['tags']:
                    cache.memory['tags'][tag] += 1
                else:
                    cache.memory['tags'][tag] = 1
        cache.dump()
        if 'to_view' in cache.memory:
            if photo in cache.memory['to_view']:
                cache.memory['to_view'].remove(photo)
        if 'new' in cache.memory:
            if photo in cache.memory['new']:
                del cache.memory['new'][photo]
    return redirect(url_for('view'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        cache.search = {}
        l = [key for key in request.form]
        for ph in cache.old:
            if search_tags(l, cache.old[ph]):
                if not ph in cache.to_delete:
                    cache.search[ph] = cache.old[ph]
    return render_template('search.html', title='Найденные фото', cache=cache.memory, len=cache.len())


@app.route('/tags')
def tags():
    return render_template('tags.html', title='Тэги', cache=cache.memory, len=cache.len())


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


@app.route('/arch')
def arch():
    return send_file("D:\\Share\\Сканер.zip",  as_attachment=True)

app.run(debug=True, host="0.0.0.0")