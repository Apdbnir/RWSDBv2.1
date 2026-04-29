# BerkeleyDB Setup Guide for WSL (Ubuntu on Windows)

This guide explains how to set up BerkeleyDB support on WSL (Windows Subsystem for Linux).

## Prerequisites

- WSL installed with Ubuntu
- Python 3.8+ installed on WSL
- PostgreSQL accessible from WSL

## Quick Setup (Automated)

```bash
# Navigate to backend directory
cd /path/to/RWSDBv2.1/backend

// cd /mnt/c/VS_Code/RWSDBv2.1/backend

# Make script executable
chmod +x setup_berkeleydb_wsl.sh

# Run setup script
./setup_berkeleydb_wsl.sh
```

## Manual Setup

If you prefer to install manually, follow these steps:

### Step 1: Install BerkeleyDB C Library

```bash
sudo apt-get update
sudo apt-get install -y libdb-dev libdb5.3 libdb5.3-dev
```

### Step 2: Install Python Package

```bash
# If using a virtual environment, activate it first
# source venv/bin/activate

pip install bsddb3
```

### Step 3: Install All Project Dependencies

```bash
pip install -r backend/requirements.txt
```

## Verify Installation

Test if BerkeleyDB is properly installed:

```bash
python3 -c "
try:
    from berkeleydb import db
    print('✓ berkeleydb package installed')
except ImportError:
    try:
        import bsddb3
        print('✓ bsddb3 package installed')
    except ImportError:
        print('✗ BerkeleyDB not installed')
        exit(1)
"
```

## Running the Converter

Once BerkeleyDB is installed, you can convert PostgreSQL tables to BerkeleyDB format:

```bash
# From the project root
python backend/berkeleydb_converter.py
```

This will convert all tables from PostgreSQL to BerkeleyDB format in the `berkeleydb/` directory.

## Running the Backend Server in WSL

To start the REST API backend using WSL Ubuntu, run:

```bash
# From the project root in WSL
cd /mnt/c/VS_Code/RWSDBv2.1/backend
chmod +x run_wsl.sh
./run_wsl.sh
```

If you prefer not to use the helper script, start the server directly:

```bash
cd /mnt/c/VS_Code/RWSDBv2.1/backend
python3 __main__.py
```

When running in WSL, the default `backend/config.json` uses a repository-relative BerkeleyDB path:

```json
{
  "admin_password": "4444",
  "database_type": "berkeleydb",
  "bdb_path": "../berkeleydb"
}
```

The backend will then use the WSL-mounted Windows path `/mnt/c/VS_Code/RWSDBv2.1/berkeleydb`.

## Troubleshooting

### Error: "No module named 'bsddb3'"

Make sure you installed the Python package:
```bash
pip install bsddb3
```

### Error: "libdb not found"

Install the BerkeleyDB C library:
```bash
sudo apt-get install libdb-dev
```

### Permission denied errors

If you get permission errors, you might need to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install bsddb3
```

## Notes

- BerkeleyDB native libraries have **limited Windows support**
- On native Windows (not WSL), the converter falls back to JSON export mode
- WSL provides full BerkeleyDB support since it runs on Linux
- The converter automatically detects if BerkeleyDB is available and uses JSON as fallback
