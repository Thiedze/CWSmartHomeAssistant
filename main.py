import json

import homematicip
from flask import Flask
from homematicip.home import Home

config = homematicip.find_and_load_config_file()

home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)

app = Flask(__name__)


def get_heating_thermostat_as_json(device):
    return device._rawJSONData


@app.route('/homematic/devices')
def homematic_devices():
    home.get_current_state()
    response = []
    for group in home.groups:
        room = {
            "room": group.label,
            "devices": []
        }
        if group.groupType == "META":
            for device in group.devices:
                room["devices"].append(get_heating_thermostat_as_json(device))

            response.append(room)
    response = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/homematic/devices/<device_id>')
def homematic_device(device_id):
    home.get_current_state()
    for group in home.groups:
        if group.groupType == "META":
            for device in group.devices:
                if device.id == device_id:
                    return app.response_class(
                        response=json.dumps(get_heating_thermostat_as_json(device)),
                        status=200,
                        mimetype='application/json')
    return app.response_class(
        response=None,
        status=404,
        mimetype='application/json')


if __name__ == '__main__':
    app.run()
