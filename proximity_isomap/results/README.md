# Numerical results and provenance

Every numbered subfolder contains a status README and the available metrics. For EXP-001, original five-radius smoke CSV/JSON are copied byte-for-byte from the prior GitHub tree.

For EXP-002–008, smaller CSVs are newly transcribed from historical discussions/repository aggregate summaries where available; **they are not original raw experiment CSV/NPZ files**, and should be tagged `historical_transcription`. Repeating a result after importing source requires a new immutable run folder with source SHA, seed, config, Python/dependency versions, data-generation parameters and manifest.

The reported global separation method uses a diagnostic synthetic-label-informed radius in EXP-005–008. Thus those reported values are not unsupervised held-out performance.
