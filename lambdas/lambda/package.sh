mkdir -p $BUILD_DIR

poetry export --only lambda -f requirements.txt --output "$LAMBDA_DIR/requirements.txt"

pip install \
    --platform manylinux2014_x86_64 \
    --target=$BUILD_DIR \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    -r requirements.txt

cp ./* $BUILD_DIR
zip -r $BUILD_DIR $OUTPUT_ZIP
rm -r $BUILD_DIR
