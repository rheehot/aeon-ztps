#!/usr/bin/python
from flask import request, send_from_directory

from aeon_ztp_app import app
import ztp_celery
import ztp_api_devices

__all__ = ['app']


@app.route('/downloads/<path:filename>', methods=['GET'])
def static_file(filename):
    return send_from_directory('/opt/aeon-ztp/downloads', filename)


@app.route('/api/bootconf/<os_name>')
def nxos_bootconf(os_name):
    return send_from_directory('static', '%s-boot.conf' % os_name)


@app.route('/api/register/<os_name>', methods=['GET', 'POST'])
def nxos_register(os_name):
    from_ipaddr = request.args.get('ipaddr') or request.remote_addr
    ztp_celery.ztp_bootstrapper.delay(os_name=os_name, target_ipaddr=from_ipaddr)
    return ""

