from flask import Flask, jsonify, abort, make_response, request, url_for
app = Flask(__name__)
import host_discoverer as hd
import ping_logger as pl


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/<string:snmp_host>", methods=['GET'])
def get_task(snmp_host):
    networks = hd.get_networks(snmp_host)
    print(networks)
    hosts = hd.scan_networks(networks)
    rh, unrh = pl.ping_log(hosts)
    return jsonify({'reachable' : rh, 'unreachable' : unrh})



if __name__ == '__main__':
    app.run(host='0.0.0.0')
