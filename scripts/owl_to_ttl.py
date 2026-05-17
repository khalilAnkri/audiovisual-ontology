"""
Convert audiovisual-ontology.owl (OWL/XML, Protégé's native format) to Turtle.

Why this script exists:
- Protégé saves the ontology in OWL/XML syntax (with <Ontology>, <Declaration>, <Class IRI=...>).
- Apache Jena Fuseki only accepts RDF/XML, Turtle, N-Triples, JSON-LD, etc.
- RDFLib (used by pyshacl, owlready2) cannot parse OWL/XML either.
- This script bridges the gap: it loads the OWL/XML via owlready2 (which understands it),
  exports to RDF/XML, then re-parses with RDFLib and writes Turtle.

Usage (from the repo root):
    python scripts/owl_to_ttl.py

Dependencies:
    pip install owlready2 rdflib
"""

import os
import sys
import tempfile

INPUT_OWL = "audiovisual-ontology.owl"
OUTPUT_TTL = "audiovisual-ontology.ttl"


def main():
    if not os.path.isfile(INPUT_OWL):
        print(f"ERROR: {INPUT_OWL} not found in current directory.")
        print("Run this script from the repository root.")
        sys.exit(1)

    try:
        from owlready2 import get_ontology
    except ImportError:
        print("ERROR: owlready2 not installed. Run: pip install owlready2")
        sys.exit(1)

    try:
        from rdflib import Graph
    except ImportError:
        print("ERROR: rdflib not installed. Run: pip install rdflib")
        sys.exit(1)

    print(f"Loading {INPUT_OWL} via owlready2 (OWL/XML parser)...")
    abs_path = os.path.abspath(INPUT_OWL)
    onto = get_ontology(f"file://{abs_path}").load()

    # owlready2 only supports RDF/XML output natively, so we go through a temp file
    with tempfile.NamedTemporaryFile(suffix=".rdf", delete=False) as tmp:
        rdf_path = tmp.name
    onto.save(file=rdf_path, format="rdfxml")
    print(f"  Intermediate RDF/XML written to {rdf_path}")

    print(f"Re-parsing with RDFLib and serializing to Turtle...")
    g = Graph()
    g.parse(rdf_path, format="xml")
    g.serialize(destination=OUTPUT_TTL, format="turtle")
    os.remove(rdf_path)

    print(f"OK  Converted {INPUT_OWL} -> {OUTPUT_TTL}")
    print(f"   Ontology contains {len(g)} triples.")
    print(f"   Ready to upload to Fuseki alongside out.ttl, mappings, and shapes.")


if __name__ == "__main__":
    main()
