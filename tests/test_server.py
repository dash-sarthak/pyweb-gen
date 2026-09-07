"""Preview server: serves the blog directory over loopback HTTP."""

import http.client
import threading
from pathlib import Path

from pyweb_gen.initialize import initialize
from pyweb_gen.server import make_server


def test_server_serves_index_page_over_loopback(tmp_path: Path) -> None:
    initialize(tmp_path)
    server = make_server(tmp_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = int(server.server_address[1])
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        connection.request("GET", "/")
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        connection.close()

        assert response.status == 200
        assert "Quill | Home" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
