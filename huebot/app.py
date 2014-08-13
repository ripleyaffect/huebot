
from phue import Bridge
from flask import Flask, request, abort, render_template

from utils import choose_color_hue, guess_color_from_hue


app = Flask(__name__)


BRIDGE_IP = ''  # Your bridge IP
LIGHT_IDS = [1, 2, 3]  # The IDs of the lights you want to control


bridge = Bridge(BRIDGE_IP)
bridge.connect()


@app.route('/hue/<hue>')
def set_hue(hue=0):
    try:
        hue = int(hue)
    except ValueError:
        return '{} is not a valid number in range 0 to 65535.'.format(hue)
    hue = min(2**16 - 1, hue)
    hue = hue if hue > 0 else 0
    bridge.set_light(LIGHT_IDS, 'hue', hue)
    return "Setting hue to {}".format(hue)


@app.route('/bri/<bri>')
def set_brighness(bri=0):
    try:
        bri = int(bri)
    except ValueError:
        return '{} is not a valid number in range 0 to 255.'.format(bri)
    bri = min(255, bri)
    bri = bri if bri > 0 else 0
    bridge.set_light(LIGHT_IDS, 'bri', bri)
    return "Setting brightness to {}".format(bri)


@app.route('/sat/<sat>')
def set_saturation(sat=0):
    try:
        sat = int(sat)
    except ValueError:
        return '{} is not a valid number in the range 0 to 255.'.format(sat)
    sat = min(255, sat)
    sat = sat if sat > 0 else 0
    bridge.set_light(LIGHT_IDS, 'sat', int(sat))
    return "Setting saturation to {}".format(sat)


@app.route('/set', methods=['POST'])
def set():
    # import ipdb; ipdb.set_trace()
    hue = request.json.get(u'hue') or bridge.get_light(2)['state'].get(u'hue')
    bri = request.json.get(u'bri') or bridge.get_light(2)['state'].get(u'bri')
    sat = request.json.get(u'sat') or bridge.get_light(2)['state'].get(u'sat')

    try:
        hue = int(hue)
    except ValueError:
        abort(400, 'Invalid value for hue')
    hue = min(2**16 - 1, hue)
    hue = hue if hue > 0 else 0

    try:
        bri = int(bri)
    except ValueError:
        abort(400, 'Invalid value for bri')
    bri = min(255, bri)
    bri = bri if bri > 0 else 0

    try:
        sat = int(sat)
    except ValueError:
        abort(400, 'Invalid value for sat')
    sat = min(255, sat)
    sat = sat if sat > 0 else 0

    bridge.set_light(LIGHT_IDS, {'hue': hue, 'bri': bri, 'sat': sat})

    return 'OK'


@app.route('/color/<color>')
def color(color):
    color = u'{}'.format(color).lower()

    hue = choose_color_hue(color)

    if hue is None:
        abort(400, 'color "{}" not recognized'.format(color))

    bri = 127
    sat = 200

    multiplier = 1.2 if 'very' in color else 1
    reducer = 0.8 if 'less' in color else 1
    negator = -1 if 'not' in color else 1

    if 'dark' in color:
        bri -= (100 * multiplier * reducer * negator)

    if 'gloomy' in color:
        sat -= (40 * multiplier * reducer * negator)

    if 'light' in color or 'bright' in color:
        bri += (100 * multiplier * reducer * negator)

    if 'deep' in color:
        sat += (40 * multiplier * reducer * negator)

    sat = min(sat, 255)
    sat = int(sat) if sat > 0 else 0

    bri = min(bri, 255)
    bri = int(bri) if bri > 0 else 0

    bridge.set_light(LIGHT_IDS, {'hue': hue, 'bri': bri, 'sat': sat})

    return 'Set lights to color {}'.format(color)


@app.route('/guess-color/<hue>')
def guess_color(hue):
    try:
        hue = int(hue)
    except ValueError:
        abort(400, 'Invalid value for hue')
    hue = min(2**16 - 1, hue)
    hue = hue if hue > 0 else 0

    color = guess_color_from_hue(hue)

    return 'Hue "{}" is closest to "{}"'.format(hue, color)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
