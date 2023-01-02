#!/bin/sh
cwd=$(pwd)
echo "#!/bin/sh" > predict_platform
echo "export PYTHONPATH=$cwd/lib/:\$PYTHONPATH" >> predict_platform
echo "export BOTTOM_MODEL=$cwd/models/bottom/mark_2/GradBoost/" >> predict_platform
echo "export TOP_MODEL=$cwd/models/top/GradBoost/" >> predict_platform
echo "python3 $cwd/predict_platform.py \"\$@\"" >> predict_platform
chmod 755 predict_platform
