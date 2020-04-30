from flask import Flask, render_template, jsonify
# from Echarts4.get_data import *
# 实例化flask
app = Flask(__name__)


# 注册路由
@app.route("/")
def index():
    return "Hello World"


@app.route("/test")
def test():
    return render_template('word_cloud.html')


if __name__ == '__main__':
    # 启动flask
    app.run(debug=True, host="0.0.0.0", port=5000)
