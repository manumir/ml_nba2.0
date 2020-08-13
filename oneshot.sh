python3 updater.py
cd ./data/
python3 appender.py
python3 preprocessing.py
cd ..
python3 get_today_games.py
python3 plac_preds.py
ls -l ./models/
python3 predictor.py
