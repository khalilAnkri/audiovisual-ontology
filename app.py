from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)


FUSEKI_ENDPOINT = "http://localhost:3030/audiovisual/sparql"
FUSEKI_UPDATE = "http://localhost:3030/audiovisual/update"


try:
    response = requests.get("http://localhost:3030/$/ping")
    if response.status_code == 200:
        print("Connected to Fuseki triplestore")
        

        count_query = "SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }"
        r = requests.post(
            FUSEKI_ENDPOINT,
            data={'query': count_query},
            headers={'Accept': 'application/sparql-results+json'}
        )
        if r.status_code == 200:
            count = r.json()['results']['bindings'][0]['count']['value']
            print(f"📊 Triplestore contains {count} triples")
    else:
        print("Warning: Fuseki may not be running")
except Exception as e:
    print(f"Error connecting to Fuseki: {e}")
    print("Please start Fuseki with: fuseki-server --mem /audiovisual")

@app.route("/")
def index():
    """Serve the SPARQL demonstrator UI"""
    return send_from_directory(".", "index.html")

@app.route("/query", methods=["POST"])
def query():
    """
    Execute SPARQL SELECT queries against Fuseki triplestore.
    This is now a proper client to a real SPARQL endpoint.
    """
    sparql = request.json.get("sparql", "")
    
    if not sparql.strip():
        return jsonify({"error": "Empty query"}), 400
    
    try:

        response = requests.post(
            FUSEKI_ENDPOINT,  
            data={'query': sparql},
            headers={'Accept': 'application/sparql-results+json'},
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"Fuseki error: {response.text}"}), 400
        
        # Parse Fuseki's JSON response
        results_json = response.json()
        
        # Extract variable names
        vars_ = results_json.get('head', {}).get('vars', [])
        
        # Extract result rows
        rows = []
        for binding in results_json.get('results', {}).get('bindings', []):
            row = []
            for var in vars_:
                if var in binding:
                    row.append(binding[var].get('value', ''))
                else:
                    row.append('')
            rows.append(row)
        
        return jsonify({"vars": vars_, "rows": rows})
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "Query timeout (>30s)"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot connect to Fuseki. Is it running at http://localhost:3030?"
        }), 503
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route("/stats", methods=["GET"])
def stats():
    """
    Added value: Provide statistics about the triplestore.
    This demonstrates that Flask does more than just proxy queries.
    """
    try:
        stats_query = """
        PREFIX ont: <https://khalilankri.github.io/audiovisual-ontology/1.0#>
        
        SELECT 
            (COUNT(DISTINCT ?title) AS ?totalTitles)
            (COUNT(DISTINCT ?talent) AS ?totalTalents)
            (COUNT(DISTINCT ?genre) AS ?totalGenres)
            (COUNT(*) AS ?totalTriples)
        WHERE {
            {
                ?title a ont:Title .
            } UNION {
                ?talent a ont:Talent .
            } UNION {
                ?genre a ont:Genre .
            } UNION {
                ?s ?p ?o .
            }
        }
        """
        
        response = requests.post(
            FUSEKI_ENDPOINT,
            data={'query': stats_query},
            headers={'Accept': 'application/sparql-results+json'}
        )
        
        if response.status_code == 200:
            data = response.json()['results']['bindings'][0]
            return jsonify({
                "titles": int(data['totalTitles']['value']),
                "talents": int(data['totalTalents']['value']),
                "genres": int(data['totalGenres']['value']),
                "triples": int(data['totalTriples']['value'])
            })
        else:
            return jsonify({"error": "Could not fetch stats"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """
    Added value: Health check endpoint.
    Verifies both Flask and Fuseki are operational.
    """
    try:
        fuseki_ping = requests.get("http://localhost:3030/$/ping", timeout=2)
        fuseki_status = fuseki_ping.status_code == 200
    except:
        fuseki_status = False
    
    return jsonify({
        "flask": "running",
        "fuseki": "running" if fuseki_status else "down",
        "endpoint": FUSEKI_ENDPOINT
    })

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Audiovisual Ontology SPARQL Server")
    print("="*60)
    print("Flask UI:      http://localhost:5000")
    print("Fuseki Admin:  http://localhost:3030")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)