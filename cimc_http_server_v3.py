import argparse
import os
import sys
from flask import Flask, abort, request, send_from_directory

app = Flask(__name__)

# Global variable for target directory
ISO_DIRECTORY = ""


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Simple Flask HTTP Server designed for Cisco CIMC Virtual Media mapping.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=80,
        help="Port number on which the HTTP server will listen",
    )

    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default="./iso",
        help="Local directory path containing files to serve",
    )

    return parser.parse_args()


@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>", methods=["GET", "HEAD"])
def serve_iso(filename):
    """Serve files and directory listings for CIMC vMedia mapping."""
    target_path = os.path.abspath(os.path.join(ISO_DIRECTORY, filename))

    # Prevent directory traversal vulnerability
    if not target_path.startswith(os.path.abspath(ISO_DIRECTORY)):
        abort(403)

    # If requested path is a directory, list all available files
    if os.path.isdir(target_path):
        try:
            files = os.listdir(target_path)
        except OSError:
            abort(500)

        html_listing = f"<h2>Available Files ({ISO_DIRECTORY})</h2><ul>"
        for entry in sorted(files):
            # Skip hidden files/directories
            if not entry.startswith("."):
                html_listing += f'<li><a href="{entry}">{entry}</a></li>'
        html_listing += "</ul>"
        return html_listing

    if not os.path.exists(target_path):
        abort(404)

    # send_from_directory handles HTTP 206 Partial Content (Range requests) natively.
    # Omitting static mimetype allows Flask/Werkzeug to dynamically detect Content-Type based on extension.
    response = send_from_directory(
        ISO_DIRECTORY,
        filename,
        conditional=True,
    )

    # Required headers for CIMC compatibility
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


if __name__ == "__main__":
    args = parse_arguments()

    # Resolve absolute path for the configured directory
    ISO_DIRECTORY = os.path.abspath(args.dir)

    if not os.path.exists(ISO_DIRECTORY):
        print(f"[INFO] Directory '{ISO_DIRECTORY}' does not exist. Creating it...")
        try:
            os.makedirs(ISO_DIRECTORY, exist_ok=True)
        except Exception as e:
            print(f"[ERROR] Could not create directory '{ISO_DIRECTORY}': {e}")
            sys.exit(1)

    print(f"Starting CIMC HTTP Server on http://0.0.0.0:{args.port}")
    print(f"Serving files from: {ISO_DIRECTORY}")
    print("Press Ctrl+C to stop.\n")

    # Run Flask server with multithreading enabled for concurrent sector access by CIMC
    app.run(host="0.0.0.0", port=args.port, threaded=True)