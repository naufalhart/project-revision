from flask import Flask, render_template, abort
import json

app = Flask(__name__)

with open("data.json") as f:
    COURSES = json.load(f)

def find_page(path_segments, current_node):
    # Base case: jika tidak ada path segments tersisa
    if not path_segments:
        return current_node
    
    # Ambil segment pertama dan segments sisanya
    current_segment = path_segments[0]
    remaining_segments = path_segments[1:]
    
    # Jika current_node adalah dict dan segment ada di dalamnya
    if isinstance(current_node, dict) and current_segment in current_node:
        return find_page(remaining_segments, current_node[current_segment])
    
    return None

@app.route("/", defaults={"subpath": ""})
@app.route("/<path:subpath>")
def course_page(subpath):
    # Buat list path segments, filter string kosong
    path_segments = [seg for seg in subpath.split("/") if seg]
    
    # Cari halaman yang sesuai
    page = find_page(path_segments, COURSES)
    
    if page is not None:
        # Tambahkan breadcrumb tracking
        breadcrumb = "/".join(path_segments) if path_segments else ""
        return render_template(
            "layout.html", 
            page=page, 
            subpath=breadcrumb
        )
    abort(404)