print("Fixing namespace in shapes.ttl...")

with open("shapes.ttl", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the ontology namespace
old_ns = "http://www.semanticweb.org/antoi/ontologies/2026/2/audiovisual-ontology"
new_ns = "https://khalilankri.github.io/audiovisual-ontology/1.0"

# Fix the shapes namespace
old_shapes = "http://www.semanticweb.org/antoi/shapes/"
new_shapes = "https://khalilankri.github.io/audiovisual-ontology/shapes/"

corrected = content.replace(old_ns, new_ns)
corrected = corrected.replace(old_shapes, new_shapes)

with open("shapes-CORRECTED.ttl", "w", encoding="utf-8") as f:
    f.write(corrected)

print(f"✅ Fixed namespace in shapes.ttl")
print(f"✅ Saved as: shapes-CORRECTED.ttl")
print(f"Ontology namespace: {content.count(old_ns)} replacements")
print(f"Shapes namespace: {content.count(old_shapes)} replacements")