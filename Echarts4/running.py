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

# @app.route("/show_pyecharts")
# def show_pyecharts():
#     bar = (
#      Bar().add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]).add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#      )
#      # print(bar.render_embed())
#     # print(bar.dump_options())
#     return render_template(
#       "show_pyecharts.html",
#        bar_data=bar.dump_options()
# )


if __name__ == '__main__':
    # 启动flask
    app.run(debug=True, host="0.0.0.0", port=5000)
