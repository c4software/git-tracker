from extended_BaseHTTPServer import serve,route

@route("/get_worker",["GET"])
def main(**kwargs):
    return "Hello Wrapper"

if __name__ == '__main__':
    serve(ip="0.0.0.0", port=5000)
