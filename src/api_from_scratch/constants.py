from pathlib import Path

"""
Dev note: Some of these variables are purely for dev/stopgap purposes, but any
long-term required depends should be specified by envs and read in as part of
the build/deployment process
"""

FILEPATH_DB = Path(__file__).parent / "db/testing_cache/db.json"
FILEPATH_DB_TESTING = Path(__file__).parent / "db/testing_cache/testing.json"
