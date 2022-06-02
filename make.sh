#!/bin/sh
cwd=$(pwd)
echo "#!/bin/sh" > predict_platform
echo "export PYTHONPATH=$cwd/lib/:\$PYTHONPATH" >> predict_platform
echo "export PLATFORM_MODEL=$cwd/models/reduced/RandomForestClassifier/" >> predict_platform
echo "python3 $cwd/predict_platform.py \"\$@\"" >> predict_platform
chmod 755 predict_platform
