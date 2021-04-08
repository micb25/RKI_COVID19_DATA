
# x-axis setup
unset xlabel
set yrange [0: 1000 < * < 90000000]

set label 1  at graph 0.99, 0.95 sprintf("{/:Bold %s}", REGION) right textcolor ls 10
set label 2  at graph 0.99, 0.89 update_str font ",12" right textcolor ls 10

plot  \
	[xmin:xmax] 1/0 notitle, \
	\
	1/0 with lines ls PLOT_STYLE2 title PLOT_TITLE2, \
	1/0 with lines ls PLOT_STYLE1 title PLOT_TITLE1, \
	\
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $5}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):($2) with lines ls PLOT_STYLE1 notitle, \
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $11}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):($2) with lines ls PLOT_STYLE2 notitle
