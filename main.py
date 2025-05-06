from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COOKIES = {
    "lang": "en",
    "_ga_06ZNKL8C2E": "GS1.1.1741174461.2.0.1741174461.60.0.0",
    "ndut_fmt": "365E95EC55679EDC29627AA5156EE3EFF145B4DCEF1BA981111FA4ED88B55B2D",
    "ndus": "YTTA7vCteHui2S2olNc2NRnqmjM2DG62Qi8B90lf",
    "_ga": "GA1.1.8713418.1741172314",
    "__bid_n": "19565f4b010ed5c2674207",
    "__stripe_mid": "bc9dd353-0691-4fa4-bc41-64fde663c45b33bfa2",
    "_ga_HSVH9T016H": "GS2.1.s1746498603$o2$g0$t1746498603$j0$l0$h0",
    "browserid": "AcP3W2ecm2WXgtJ5CYkqvBSXefk-i7KaxBGYlGCWr_CIEFFIAPsC3K8i_bo=",
    "csrfToken": "UMQobX4nKoVhyGWA9dGqaz9T",
    "g_state": '{"i_l":0}',
    "PANWEB": "1"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


@app.route('/')
def docs():
    return '''
    <h2>🧾 Terabox Video Downloader API</h2>
    <p>✨ <b>Credit:</b> <a href="https://t.me/AnshAPi">@AnshAPi</a></p>
    <p>🧑‍💻 <b>Dev:</b> cyber_ansh</p>
    <p><b>Usage:</b></p>
    <pre>GET /download?url=TERABOX_LINK</pre>
    <p>Example:</p>
    <pre>/download?url=https://www.1024terabox.com/s/1abcXYZexample</pre>
    '''


@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        session = requests.Session()
        session.cookies.update(COOKIES)
        session.headers.update(HEADERS)

        res = session.get(url)
        if "window.location.href" not in res.text:
            return jsonify({"error": "Invalid or unsupported link"}), 400

        # Extract download link (simplified logic, you can expand with regex if needed)
        download_link = res.url
        return jsonify({
            "status": "success",
            "download_link": download_link,
            "credit": "@AnshAPi",
            "dev": "cyber_ansh"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000)
