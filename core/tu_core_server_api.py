import flask
import settings

# create application
application = flask.Flask("tu_core_server")

# global variables
telemetry_data = {}


# put telemetry endpoint
@application.route("/telemetry_post", methods=["POST"])
def telemetry_post():
    global telemetry_data
    telemetry_data = flask.request.json
    print(telemetry_data)
    return "success", 200


# get telemetry endpoint
@application.route("/telemetry_get", methods=["GET"])
def telemetry_get():
    global telemetry_data
    return flask.jsonify(telemetry_data), 200


# prevent data leakage
@application.errorhandler(404)
def page_not_found(error):
    return "restricted", 404


# only run the server when direct call
if __name__ == "__main__":
    # start core server
    application.run(debug=True, host=tu_settings.core_server_ip, port=tu_settings.core_server_port, threaded=True)
