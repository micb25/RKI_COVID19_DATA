# RKI_COVID19_DATA

Prozessierte RKI COVID19 Dataframes, die um einige Felder erweitert wurden:

- Altersgruppe2 (aus alten Dump Ende April bzw. Zuordnung über RKI SurvStat)
- timestamp_reporting (Meldedatum)
- timestamp_ref (Erkrankungsbeginn bzw. Meldedatum)
- timestamp_recovered (Zeitpunkt der Genesung)
- timestamp_announced (Zeitpunkt wann Fall veröffentlicht wurde)
- announcement_flagged (wenn 1: timestamp_announced womöglich ungenau)
- timestamp_death_earliest (frühster Todeszeitpunkt)
- timestamp_death_latest (spätester Todeszeitpunkt)
- timestamp_death (zugeordneter Todeszeitpunkt)
- day_of_death_flagged (wenn 1: timestamp_death womöglich ungenau)
