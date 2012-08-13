#-*- coding:UTF-8-*-
from flask import Flask, make_response, render_template
from config import ROOT_DIR
from os import path
import os
import time

app = Flask(__name__)

class fileModel():
    name = None
    size = None
    date = None
    def __init__(self, name, size, date):
        self.name = name
        self.size = size
        self.date = date
    def __unicode__(self):
        return self.name


def list_abs_dir(abspath):
    retval_files_dirs = []
    try:
        files_and_dirs = os.listdir(abspath)
    except:
        return None
    for x in files_and_dirs:
        if x[0] == '.':
            continue
        elif os.path.isdir(os.path.join(abspath, x)):
            retval_files_dirs.append(x.decode('UTF-8') + u'/')
        else:
            retval_files_dirs.append(x.decode('UTF-8'))
    return retval_files_dirs

def list_file_stat(dir_abspath, files_and_dirs):
    files_and_dirs_set = []
    if not files_and_dirs:
        return None
    for x in files_and_dirs:
        try:
            info = os.stat(os.path.join(dir_abspath, x))
        except:
            files_and_dirs_set.append(x.decode('UTF-8'), u'N/A(无权限)', u'N/A(无权限)')
        else:
            value = fileModel(x, 
                              info.st_size,
                              time.strftime("%Y-%m-%d", time.localtime(info.st_mtime)))
            files_and_dirs_set.append(value)
    return files_and_dirs_set

@app.route('/')
def home():
    abspath =  os.path.abspath(ROOT_DIR)
    files_set = list_file_stat(abspath, list_abs_dir(abspath))
    if not files_set:
        response = make_response(render_template('not_found.htm'), 404)
    else:
        response = make_response(render_template('basic.htm',
                                                  site_path='/',
                                                  files = files_set)
        )
    return response

@app.route('/<path:Path>')
def index(Path):
    abspath = os.path.abspath(os.path.join(ROOT_DIR, Path))
    if os.path.isdir(abspath):
        files_set = list_file_stat(abspath, list_abs_dir(abspath))
        if not files_set:
            response = make_response(render_template('not_found.htm'), 404)
        else:
            response = make_response(render_template('basic.htm',
                                                      site_path=Path,
                                                      files = files_set)
            )
    else:
        have_read_access = os.access(abspath, os.R_OK)
        if have_read_access:
            response = make_response(abspath)
            response.headers['Content-Type']='application/octet-stream'
        else: 
            response = make_response(render_template('not_found.htm'), 404)
    return response

if __name__ == '__main__':
    app.run(debug = True)
