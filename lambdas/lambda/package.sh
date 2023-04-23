mkdir -p "$BUILD_DIR"
mkdir -p "dist"

poetry export --only lambda -f requirements.txt --output "$BUILD_DIR/requirements.txt"

pip install \
    --platform manylinux2014_x86_64 \
    --target="$BUILD_DIR" \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    -r "$BUILD_DIR/requirements.txt"

cp "$LAMBDA_DIR/"* "$BUILD_DIR/"
(cd "$BUILD_DIR" && zip -r - ./) > $OUTPUT_ZIP
rm -r "$BUILD_DIR"
