from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def json_rpc_handler():
    try:
        data = request.get_json()
        if "method" in data and "params" in data:
            method = data["method"]
            params = data["params"]
            result = handle_json_rpc_request(method, params)
            response = {"jsonrpc": "2.0", "result": result, "id": data.get("id")}
        else:
            response = {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": data.get("id")}
    except Exception as e:
        response = {"jsonrpc": "2.0", "error": {"code": -32603, "message": "Internal error", "data": str(e)}, "id": data.get("id")}

    return jsonify(response)

def handle_json_rpc_request(method, params):
    if method == "ConvertDollar":
        return params.get("a", 0)*3
    if method =="ConvertEuro":
        return params.get("a", 0) * 3.5

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
