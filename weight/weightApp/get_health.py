from flask import Flask, Response, render_template
app = Flask(__name__,)

@app.route('/health')
def get_health():
    return Response("OK", status=200, mimetype="text")