# poke2vec

## download
```bash
python download.py top_users data gen7battlespotsingles
python download.py replay_ids data data/gen7battlespotsingles_top_users.json
python download.py battle_logs data data/gen7battlespotsingles_replay_ids.json
```

## parse_logs
```bash
python parse_logs.py data data/gen7vgc2018_battle_logs.json
```

## preprocess
```bash
python poke2vec.py preprocess data data/gen7battlespotsingles_parsed_battle_logs.json
```

## train
```bash
python poke2vec.py train data/gen7battlespotsingles_dataset.json 256
```

