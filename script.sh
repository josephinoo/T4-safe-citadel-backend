find . -name "*.py" ! -path "./venv/*" ! -path "./alembic/*" -exec pylint {} \;
