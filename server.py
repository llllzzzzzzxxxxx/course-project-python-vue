from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 存储视频信息的字典
video_data = {}
# 存储视频文件路径的字典
video_paths = {}

@app.route('/api/info/<bvid>', methods=['GET'])
def get_video_info(bvid):
    """
    获取视频信息
    :param bvid: 视频BV号
    :return: 视频信息JSON
    """
    try:
        # 这里应该是从B站API获取视频信息的逻辑
        # 示例数据
        video_data[bvid] = {
            "code": 0,
            "data": {
                "title": "示例视频标题",
                "pic": "https://i0.hdslb.com/bfs/archive/sample.jpg",
                "owner": {"name": "示例UP主"},
                "duration": 3600
            }
        }
        return jsonify(video_data[bvid])
    except Exception as e:
        return jsonify({"code": -1, "message": str(e)}), 500

@app.route('/api/file-path/<bvid>', methods=['GET'])
def get_file_path(bvid):
    """
    获取视频文件路径
    :param bvid: 视频BV号
    :return: 文件路径JSON
    """
    try:
        # 这里应该是获取视频文件路径的逻辑
        # 示例路径
        video_paths[bvid] = "C:\\Users\\Public\\Videos\\sample.mp4"
        return jsonify({"code": 0, "data": video_paths[bvid]})
    except Exception as e:
        return jsonify({"code": -1, "message": str(e)}), 500

@app.route('/proxy-image', methods=['GET'])
def proxy_image():
    """
    代理获取B站图片，解决跨域问题
    :return: 图片数据
    """
    try:
        image_url = request.args.get('url')
        if not image_url:
            return "Missing image URL", 400
        
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content, response.status_code, {'Content-Type': response.headers['Content-Type']}
    except Exception as e:
        return str(e), 500

@app.route('/api/video', methods=['POST'])
def handle_video():
    """
    处理视频下载请求
    :return: 下载结果JSON
    """
    try:
        data = request.json
        bvid = data.get('bvid')
        if not bvid:
            return jsonify({"code": -1, "message": "Missing bvid"}), 400
        
        # 这里应该是视频下载的逻辑
        # 示例返回
        return jsonify({
            "code": 0,
            "download_url": f"C:\\Users\\Public\\Videos\\{bvid}.mp4"
        })
    except Exception as e:
        return jsonify({"code": -1, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)