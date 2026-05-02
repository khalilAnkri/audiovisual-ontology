
# Audiovisual Content Ontology

An ontology for modeling audiovisual content including movies, TV shows, talents, and their relationships.

## Namespace

**Ontology IRI:** `https://khalilankri.github.io/audiovisual-ontology/1.0#`

This ontology is deployed and accessible at the above URL.

## Architecture
┌─────────────────────────────────────┐
│  Flask Web Application (Port 5000)  │
│  - SPARQL Query Interface           │
│  - Statistics Endpoint              │
│  - Health Monitoring                │
└─────────────────┬───────────────────┘
│ HTTP/SPARQL
▼
┌─────────────────────────────────────┐
│  Apache Jena Fuseki (Port 3030)     │
│  - SPARQL Endpoint                  │
│  - Triplestore (In-Memory/TDB2)     │
└─────────────────┬───────────────────┘
│
▼
┌─────────────────────────────────────┐
│  RDF Data                           │
│  - Ontology Schema (.owl)           │
│  - Instance Data (.ttl)             │
│  - R2RML Mappings (.ttl)            │
└─────────────────────────────────────┘