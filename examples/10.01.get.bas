10 GET A$
20 IF A$ = "" THEN 10
40 IF A$ = CHR$(13) THEN 70
50 IF A$ = CHR$(8) THEN 10
60 PRINT "PULSASTE: "; A$
70 PRINT "FIN DE LA ENTRADA"
80 PRINT "PULSASTE: "; A$