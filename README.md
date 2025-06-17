# Bibliographic Data Processing Pipeline

## Overview

This project implements a robust pipeline for ingesting, processing, and storing bibliographic data from various academic sources, including Scopus and Web of Science (WoS). It is designed to handle large datasets efficiently through parallel processing and bulk database operations. The system supports both full data refreshes and incremental updates.

## Features

*   **Multiple Data Sources**: Currently supports Scopus and Web of Science. Extensible for other sources.
*   **Parallel Processing**: Leverages multiple CPU cores to speed up the ingestion of large data files.
*   **Bulk Database Operations**: Uses BCP (Bulk Copy Program) files and staging tables for efficient data loading into a PostgreSQL database.
*   **Data Refresh and Update**: Capable of performing full data refreshes or incremental updates to existing datasets.
*   **Modular Design**: Python-based ingestion logic is separated for each data source, allowing for easier maintenance and extension.
*   **Shell-Based Orchestration**: Uses shell scripts to control the overall workflow, manage environment settings, and execute database operations.

## Core Components

*   **`controller/process.sh`**:
    *   The main entry point to initiate the data processing pipeline.
    *   Orchestrates all steps from environment setup to final data indexing.
    *   Manages parallel execution of Python ingestion scripts.

*   **`libbiblio/ingest_data.py`**:
    *   The central Python script responsible for data ingestion.
    *   Dynamically loads parsers and ingestors based on the data source (e.g., Scopus, WoS).
    *   Coordinates with a database table (`BibliometricsFileStatus`) to manage distributed processing of input files.
    *   Transforms raw data into BCP files for efficient database loading.

*   **`db/` Directory**:
    *   Contains all database-related scripts and schema definitions.
    *   `set_biblio_db_envs.sh`: Configures database connection parameters.
    *   Provider-specific subdirectories (e.g., `db/scopus/`, `db/wos/`) hold SQL scripts for:
        *   Creating/recreating staging and production tables.
        *   Processing data from staging tables (transformations, cleaning).
        *   Creating database indexes.

*   **`libbiblio/sources/` Directory**:
    *   Contains provider-specific Python modules for parsing and ingesting data (e.g., `scopus_ingestor.py`, `wos_parser.py`).

## Basic Setup and Usage

### Prerequisites

*   **Python 3.8+**
*   **Poetry**: For Python dependency management (implied by `poetry run` commands).
*   **PostgreSQL Client (`psql`)**: For database interactions by shell scripts.
*   **PostgreSQL Server**: A running instance where the data will be stored.
*   Standard Unix utilities (bash, sed, nproc, etc.).

### Environment Configuration

Before running the pipeline, you need to configure the database connection details. This is typically done by editing and sourcing the `db/set_biblio_db_envs.sh` script. Essential variables include:

*   `POSTGRES_DB`: The name of the database.
*   `POSTGRES_SERVER`: The hostname or IP address of the PostgreSQL server.
*   `POSTGRES_USER`: The database username.
*   `POSTGRES_PORT_5432_TCP_ADDR` (or similar, depending on exact setup in `set_biblio_db_envs.sh`): Often used as an alternative way to specify the server.
*   `POSTGRES_PASSWORD`: The database password.

Ensure this script is executable and its variables are exported to the environment where `process.sh` will run.

### Running the Pipeline

The main pipeline is started using the `controller/process.sh` script.

**Command Structure:**

```bash
./controller/process.sh <provider> <source_dir> <work_dir> <update_refresh>
```

**Arguments:**

*   `<provider>`: The data source to process (e.g., `scopus`, `wos`).
*   `<source_dir>`: The absolute path to the directory containing the raw input data files (e.g., ZIP or XML files from Scopus/WoS).
*   `<work_dir>`: An absolute path to a working directory where temporary files (like BCP files and extracted updates) will be stored. This directory will be cleaned by `clean_env.sh`.
*   `<update_refresh>`:
    *   `refresh`: Performs a full refresh. Staging tables for the provider are recreated, and all data from `source_dir` is processed.
    *   `update`: Performs an update. The system attempts to process only new or changed files.

**Example:**

```bash
# Ensure environment variables are set
# source ./db/set_biblio_db_envs.sh

# Example for a full refresh of Scopus data
./controller/process.sh scopus /path/to/scopus_data_zips /tmp/scopus_processing_work refresh

# Example for an update of WoS data
./controller/process.sh wos /path/to/wos_data_zips /tmp/wos_processing_work update
```

### Input Data

*   Place raw data files (e.g., `.zip` archives containing XMLs, or individual `.xml` files) in the specified `<source_dir>`.
*   The system identifies files to process based on the `BibliometricsFileStatus` table, which is populated by `process.sh` at the start of a run.

## Project Structure

```
.
├── controller/         # Shell scripts for pipeline orchestration
│   ├── process.sh      # Main pipeline script
│   ├── load_daemon.sh  # Background script for loading BCP data
│   ├── ...
├── db/                 # Database related scripts and schemas
│   ├── set_biblio_db_envs.sh # DB environment configuration
│   ├── scopus/           # Scopus-specific SQL scripts
│   ├── wos/              # WoS-specific SQL scripts
│   ├── ...
├── libbiblio/          # Core Python library for ingestion
│   ├── ingest_data.py  # Main Python ingestion script
│   ├── file_status_handler.py # Manages file processing status in DB
│   ├── sources/          # Provider-specific Python modules
│   │   ├── scopus/
│   │   └── wos/
│   └── ...
├── biblio.py           # (Potentially an entry point or utility script)
├── env_template        # Template for environment variables
├── TECHNICAL_DOCUMENTATION.md # Detailed technical docs
└── README.md           # This file
```

## Further Details

For a more in-depth understanding of the system architecture, data flow, and specific script functionalities, please refer to the `TECHNICAL_DOCUMENTATION.md` file.
