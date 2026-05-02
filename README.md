# Audiovisual Content Ontology

An ontology for modeling audiovisual content including movies, TV shows, music, and related media. This project demonstrates semantic web technologies including ontology design, R2RML mappings, SPARQL querying, and triplestore deployment.

---

## Namespace URI

**Ontology IRI:** `https://khalilankri.github.io/audiovisual-ontology/1.0#`

**Data IRI:** `https://khalilankri.github.io/audiovisual-ontology/data/`

This ontology is deployed and accessible at GitHub Pages.

---

## Architecture
┌─────────────────────────────────────────┐
│  Flask Web Application (Port 5000)      │
│  ├─ SPARQL Query Interface              │
│  ├─ Statistics Endpoint (/stats)        │
│  ├─ Health Monitoring (/health)         │
│  └─ Error Handling & Validation         │
└────────────────┬────────────────────────┘
│ HTTP/SPARQL
▼
┌─────────────────────────────────────────┐
│  Apache Jena Fuseki (Port 3030)         │
│  ├─ SPARQL Endpoint                     │
│  ├─ Triplestore (In-Memory/TDB2)        │
│  ├─ SPARQL 1.1 Compliant                │
│  └─ ~10,000 triples                     │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│  RDF Data                               │
│  ├─ Ontology Schema (.owl)              │
│  ├─ Instance Data (.ttl)                │
│  ├─ R2RML Mappings (.ttl)               │
│  └─ SHACL Shapes (.ttl)                 │
└─────────────────────────────────────────┘

**Key Design Decisions:**
- **Separation of Concerns:** Flask handles UI/UX, Fuseki handles data storage and querying
- **Real SPARQL Endpoint:** Standards-compliant, accessible by any SPARQL client
- **Namespace Separation:** Hash-based URIs for ontology classes (`#`), slash-based for instances (`/`)
- **Added Value:** Flask provides statistics, health checks, and user-friendly error handling beyond basic query proxying

---

## Ontology Overview

### Core Classes

- **Title** - Audiovisual works (movies, TV shows, etc.)
- **Talent** - Individuals involved in production (actors, directors, etc.)
- **Participation** - Bridge class linking Talent to Title with specific roles
- **Genre** - Content classification (Action, Drama, Comedy, etc.)
- **ContentType** - Media format (movie, TV series, short, etc.)
- **Category** - Professional category (actor, actress, director, etc.)
- **Role** - Character or position played
- **AlternativeTitle** - Regional or alternative names for titles
- **Region** - Geographic regions for title distribution
- **TitleType** - Type of alternative title

### Key Properties

**Object Properties:**
- `isClassifiedAs` - Links Title to ContentType
- `hasGenre` - Links Title to Genre
- `contains` - Links Title to Participation
- `participatesIn` - Links Talent to Participation
- `plays` - Links Participation to Role
- `as` - Links Participation to Category
- `isAka` - Links Title to AlternativeTitle
- `isFrom` - Links AlternativeTitle to Region
- `hasType` - Links AlternativeTitle to TitleType

**Data Properties:**
- `primaryTitle` - Main title name
- `talentName` - Talent's name
- `genreName` - Genre name
- `roleName` - Role/character name
- `categoryName` - Category name
- `regionName` - Region name
- `startYear` - Year of release
- `job` - Job description in participation

All instances include `rdfs:label` for human-readable display.

---

## Setup & Installation

### Prerequisites
- **Java 11+** (for Fuseki)
- **Python 3.8+**
- **Apache Jena Fuseki** ([Download](https://jena.apache.org/download/))

### Step 1: Start Fuseki Triplestore

**Windows:**
```bash
cd apache-jena-fuseki-X.X.X
fuseki-server.bat --mem /audiovisual
```

**Linux/Mac:**
```bash
cd apache-jena-fuseki-X.X.X
./fuseki-server --mem /audiovisual
```

Fuseki will be available at: **http://localhost:3030**

### Step 2: Load Data into Fuseki

**Option A: Web Interface (Recommended)**
1. Go to http://localhost:3030
2. Click **"manage datasets"** → **"audiovisual"** → **"upload data"**
3. Upload the following files in order:
   - `out.ttl` (instance data)
   - `audiovisual_mappings.ttl` (R2RML mappings)
   - `shapes.ttl` (SHACL constraints)

**Option B: Command Line (PowerShell)**
```powershell
Invoke-WebRequest -Uri "http://localhost:3030/audiovisual/data" -Method POST -InFile "out.ttl" -ContentType "text/turtle" -UseBasicParsing

Invoke-WebRequest -Uri "http://localhost:3030/audiovisual/data" -Method POST -InFile "audiovisual_mappings.ttl" -ContentType "text/turtle" -UseBasicParsing

Invoke-WebRequest -Uri "http://localhost:3030/audiovisual/data" -Method POST -InFile "shapes.ttl" -ContentType "text/turtle" -UseBasicParsing
```

**Verify Data Loaded:**
- Go to http://localhost:3030 → Click "audiovisual" → "info"
- Should show ~10,000 triples

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
Flask==3.0.0
requests==2.31.0
rdflib==7.0.0

### Step 4: Start Flask Application

```bash
python app.py
```

**Expected Output:**
Audiovisual Ontology SPARQL Server
Flask UI:      http://localhost:5000
Fuseki Admin:  http://localhost:3030
Connected to Fuseki triplestore
Triplestore contains 9957 triples

Running on http://0.0.0.0:5000


Access the application at: **http://localhost:5000**

---

## Endpoints

### Flask Application Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | SPARQL query interface with predefined queries |
| `/query` | POST | Execute SPARQL queries against Fuseki |
| `/stats` | GET | Database statistics (titles, talents, genres, triple count) |
| `/health` | GET | Health check for Flask and Fuseki connectivity |

### Fuseki Endpoints

| Endpoint | Description |
|----------|-------------|
| `http://localhost:3030/` | Fuseki admin interface |
| `http://localhost:3030/audiovisual/sparql` | SPARQL query endpoint |
| `http://localhost:3030/audiovisual/update` | SPARQL update endpoint |
| `http://localhost:3030/audiovisual/data` | Graph store protocol (upload data) |

---

## Regenerating RDF from Database

If you need to regenerate the RDF data from the source database using R2RML mappings:

### Prerequisites
- R2RML processor JAR file
- Database with audiovisual data
- `audiovisual_mappings.ttl` (R2RML mappings)
- `config.properties` (database connection)



### Generate RDF

```bash
java -jar r2rml.jar config.properties
```

This creates `out.ttl` with the correct namespace and `rdfs:label` properties.

---


---


## Authors

- **ANKRI Mohamed-Khalil**
- **MICHON Charlotte**
- **PAULIS Antoine**

**Course:** Knowledge Representation and Reasoning  
**Institution:** [Your University Name]  
**Date:** May 2026

---


## Links

- **Ontology:** https://khalilankri.github.io/audiovisual-ontology/1.0
- **GitHub Repository:** https://github.com/khalilankri/audiovisual-ontology
- **Apache Jena:** https://jena.apache.org/
- **W3C SPARQL:** https://www.w3.org/TR/sparql11-query/
- **W3C SHACL:** https://www.w3.org/TR/shacl/
- **R2RML:** https://www.w3.org/TR/r2rml/



---

## Acknowledgments

- Apache Jena team for the excellent Fuseki triplestore
- W3C for semantic web standards (RDF, SPARQL, SHACL, R2RML)
- Course instructor for valuable feedback and guidance
- IMDb for providing the source data

---

**Built with semantic web technologies to demonstrate professional ontology engineering practices.** 