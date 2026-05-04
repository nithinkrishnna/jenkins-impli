from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Dockerized Application deployed via Jenkins CI/CD on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
