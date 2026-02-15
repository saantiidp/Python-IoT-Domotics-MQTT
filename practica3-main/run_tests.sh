#!/bin/bash

# Ignorar warnings deprecados
export PYTHONWARNINGS="ignore::DeprecationWarning"
export PYTHONPATH=$(pwd)

echo "Ejecutando tests con unittest..."
for file in tests/test_*.py; do
    echo "---------------------------------------------"
    echo "Ejecutando unittest en $file"
    python "$file"
done

echo "Tests unittest completados."

echo ""
echo "Ejecutando tests con pytest..."
pytest tests/ -v
echo "Tests pytest completados."
