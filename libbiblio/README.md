```console
libbiblio
├── README.md
├── __init__.py
├── db
│   ├── __init__.py
│   ├── config.py
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── models
│   │   ├── __init__.py
│   │   ├── ingestion_log.py
│   │   ├── scopus
│   │   │   ├── __init__.py
│   │   │   ├── scopus_author.py
│   │   │   ├── scopus_record.py
│   │   │   └── scopus_source.py
│   │   └── web_of_science
│   │       ├── __init__.py
│   │       ├── wos_author.py
│   │       ├── wos_record.py
│   │       └── wos_source.py
│   └── session.py
├── ingest.py
└── sources
    ├── __init__.py
    ├── common
    │   ├── __init__.py
    │   └── db_errors.py
    ├── garbage.py
    ├── scopus
    │   ├── __init__.py
    │   ├── scopus_ingestor.py
    │   └── scopus_parser.py
    └── web_of_science
        ├── __init__.py
        ├── wos_ingestor.py
        └── wos_parser.py
```