
pyinstaller -F lambda/sidecar.py

pip install \
    --platform manylinux2014_x86_64 \
    --target=$BUILD_DIR \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    -r lambda/requirements.txt

cp lambda/* $BUILD_DIR
zip -r $BUILD_DIR $OUTPUT_ZIP

rm -r $BUILD_DIR
