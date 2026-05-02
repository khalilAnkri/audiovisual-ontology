from flask import Flask, request, jsonify, send_from_directory
from rdflib import Graph
import os

app = Flask(__name__)

print("Loading out.ttl...")
g = Graph()
g.parse("out.ttl", format="turtle")
print(f"Loaded {len(g)} triples.")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/query", methods=["POST"])
def query():
    sparql = request.json.get("sparql", "")
    try:
        results = g.query(sparql)
        vars_ = [str(v) for v in results.vars]
        rows = []
        for row in results:
            rows.append([str(v) if v is not None else "" for v in row])
        return jsonify({"vars": vars_, "rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=False)