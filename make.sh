#!/bin/sh
cwd=$(pwd)
echo "#!/bin/sh" > predict_platform
echo "export PYTHON_PATH=$cwd/lib/:\$PYTHON_PATH" >> predict_platform
echo "export PLATFORM_MODEL=$cwd/models/reduced/RandomForestClassifier/" >> predict_platform
echo "python3 $cwd/predict_platform.py \"\$@\"" >> predict_platform
chmod 755 predict_platform