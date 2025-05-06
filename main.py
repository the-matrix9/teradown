from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# ✅ Credits
CREDITS = {
    "credit": "t.me/AnshAPi",
    "dev": "cyber_ansh"
}

# ✅ Headers with cookies
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": (
        "PANWEB=1; "
        "__bid_n=19565f4b010ed5c2674207; "
        "__stripe_mid=bc9dd353-0691-4fa4-bc41-64fde663c45b33bfa2; "
        "_ga=GA1.1.8713418.1741172314; "
        "_ga_06ZNKL8C2E=GS1.1.1741174461.2.0.1741174461.60.0.0; "
        "lang=en; "
        "g_state={\"i_l\":0}; "
        "ndus=YTTA7vCteHui2S2olNc2NRnqmjM2DG62Qi8B90lf; "
        "csrfToken=UMQobX4nKoVhyGWA9dGqaz9T; "
        "browserid=AcP3W2ecm2WXgtJ5CYkqvBSXefk-i7KaxBGYlGCWr_CIEFFIAPsC3K8i_bo=; "
        "_ga_HSVH9T016H=GS2.1.s1746498603$o2$g0$t1746498603$j0$l0$h0; "
        "ndut_fmt=365E95EC55679EDC29627AA5156EE3EFF145B4DCEF1BA981111FA4ED88B55B2D"
    )
}

# 📘 Documentation route
@app.route('/', methods=['GET'])
def docs():
    return jsonify({
        "name": "Terabox Video Downloader API",
        "description": "Fetch direct download link from a Terabox video URL using cookies.",
        "endpoint": "/download",
        "method": "GET",
        "params": {
            "url": "The full Terabox share link. Example: https://www.terabox.com/s/1abcXYZ"
        },
        "example_request": "/download?url=https://www.terabox.com/s/1abcXYZ",
        "sample_response": {
            "filename": "video.mp4",
            "direct_link": "https://download-link.terabox.com/file.mp4",
            "status": "success",
            "credit": "t.me/AnshAPi",
            "dev": "cyber_ansh"
        },
        **CREDITS
    })

# 🔽 Video Download logic
def get_video_links(url):
    try:
        file_id_match = re.search(r'/s/1([A-Za-z0-9_-]+)', url)
        if not file_id_match:
            return {'error': 'Invalid Terabox URL format', **CREDITS}

        file_id = '1' + file_id_match.group(1)
        api_url = f"https://www.terabox.com/share/list?app_id=250528&shorturl={file_id}&root=1"

        res = requests.get(api_url, headers=HEADERS)
        data = res.json()

        if 'list' not in data or not data['list']:
            return {'error': 'No files found or cookies expired', **CREDITS}

        file_info = data['list'][0]
        dlink = file_info.get('dlink')
        filename = file_info.get('server_filename')

        return {
            'filename': filename,
            'direct_link': dlink,
            'status': 'success',
            **CREDITS
        }

    except Exception as e:
        return {'error': str(e), **CREDITS}

# 🎯 Download Endpoint
@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required', **CREDITS}), 400

    result = get_video_links(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
