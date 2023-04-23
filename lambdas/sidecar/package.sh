mkdir -p "$BUILD_DIR"
mkdir -p "dist"

poetry export --only lambda-sidecar -f requirements.txt --output "$BUILD_DIR/requirements.txt"

pip install \
    --platform manylinux2014_x86_64 \
    --target="$BUILD_DIR/venv" \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    -r "$BUILD_DIR/requirements.txt"

$BUILD_DIR/venv/bin/pyinstaller -F "$LAMBDA_DIR/sidecar.py" --distpath "$BUILD_DIR" --workpath "$BUILD_DIR/pyinstaller"
rm -r "$BUILD_DIR/venv" "$BUILD_DIR/pyinstaller"

cp "$LAMBDA_DIR/"* "$BUILD_DIR/"
(cd "$BUILD_DIR" && zip -r - ./) > $OUTPUT_ZIP
rm -r "$BUILD_DIR"
