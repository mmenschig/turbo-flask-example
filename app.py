import threading
import random
import time
import re
import sys
from flask import Flask, render_template

from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.context_processor
def inject_load():

    if sys.platform.startswith('linux'): 
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
        print(load)
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}

# Workaround because .before_first_request decorator is deprecated with flask 2.3+
# See Application Factory mgiration guide here: https://hackersandslackers.com/flask-application-factory/
with app.app_context():
    threading.Thread(target=update_load).start()