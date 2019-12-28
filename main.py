import json

import homematicip
from flask import Flask
from homematicip.device import HeatingThermostat
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
    response = {}
    for group in home.groups:
        if group.groupType == "META":
            for device in group.devices:
                if isinstance(device, HeatingThermostat):
                    if not response.__contains__(group.label):
                        response[group.label] = []
                    response[group.label] = get_heating_thermostat_as_json(device)
    response = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
