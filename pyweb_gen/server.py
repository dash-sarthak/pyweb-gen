"""Local preview server for a built blog."""

import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DEFAULT_PORT = 8000


def make_server(root: Path, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Bind a preview server for root; port 0 asks the OS for a free port."""
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(root))
    return ThreadingHTTPServer(("", port), handler)


def serve_blog(root: Path, port: int = DEFAULT_PORT) -> None:
    """Serve the blog directory until interrupted."""
    httpd = make_server(root, port)
    bound_port = httpd.server_address[1]
    print(f"Serving {root} at http://localhost:{bound_port}/ (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
