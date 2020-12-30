
# x-axis setup
unset xlabel
set yrange [0: 1000 < * < 90000000]

set label 1  at graph 0.98, 0.10 sprintf("{/Helvetica-Bold %s}", REGION) right textcolor ls 10
set label 2  at graph 0.98, 0.04 update_str font ",12" right textcolor ls 10

plot  \
	[xmin:xmax] 1/0 notitle, \
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $5}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):($2) with linespoints ls PLOT_STYLE title PLOT_TITLE
