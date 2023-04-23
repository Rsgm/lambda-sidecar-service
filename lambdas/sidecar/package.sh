mkdir -p $BUILD_DIR

poetry export --only lambda-sidecar -f requirements.txt --output "$BUILD_DIR/requirements.txt"

pip install \
    --platform manylinux2014_x86_64 \
    --target=$BUILD_DIR \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    -r $BUILD_DIR/requirements.txt

$BUILD_DIR/bin/pyinstaller -F $LAMBDA_DIR/sidecar.py
