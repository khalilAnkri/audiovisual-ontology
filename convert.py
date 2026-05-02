import re

print("Fixing and converting OWL file...")

# Read the file as text
with open("audiovisual-ontology-M3.owx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the namespace
old_ns = "http://www.semanticweb.org/antoi/ontologies/2026/2/audiovisual-ontology"
new_ns = "https://khalilankri.github.io/audiovisual-ontology/1.0"
content = content.replace(old_ns, new_ns)

# Save the fixed OWL file
with open("audiovisual-ontology-FIXED.owl", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed namespace in OWL file")
print("✅ Saved as: audiovisual-ontology-FIXED.owl")

# Now try to convert to Turtle
try:
    from rdflib import Graph
    g = Graph()
    g.parse("audiovisual-ontology-FIXED.owl", format="xml")
    
    # Save as Turtle
    g.serialize(destination="audiovisual-ontology.ttl", format="turtle")
    print(f"✅ Converted to Turtle: {len(g)} triples")
    print("✅ Saved as: audiovisual-ontology.ttl")
    
except Exception as e:
    print(f"⚠️  Could not convert to Turtle: {e}")
    print("But the fixed OWL file is ready to upload!")