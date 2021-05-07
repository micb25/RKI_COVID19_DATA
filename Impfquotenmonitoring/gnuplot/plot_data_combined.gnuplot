
# x-axis setup
set yrange [0: 1 < * ]

set label 1  at graph 0.99, 0.95 sprintf("{/:Bold %s}", REGION) right textcolor ls 10
set label 2  at graph 0.99, 0.89 update_str font ",12" right textcolor ls 10

# fit
m = 1
n = -STATS_min
f(x) = m * x + n
fit [ xmax - 14 * 86400 : xmax ] f(x) "<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, ($5+$11)/1000000}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):($2) via m, n

vac_per_day = m * 86400

set label 6 at graph 0.03, 0.75 " " left textcolor ls 0
set label 7 at graph 0.03, 0.75 " " left textcolor ls 0
set label 8 at graph 0.03, 0.75 " " left textcolor ls 0

if ( vac_per_day > 0 ) {
	set label 3 at graph 0.03, 0.71 "{/:Bold 14-Tage-Trend (Erst- und Zweitimpfungen):}" left textcolor ls 10
	set label 4 at graph 0.06, 0.64 sprintf("%+.0f Impfungen pro Tag", 1000000 * vac_per_day) left textcolor ls 10
} else {
	set label 3 at graph 0.03, 0.75 " " left textcolor ls 0
	set label 4 at graph 0.03, 0.75 " " left textcolor ls 0
	set label 5 at graph 0.03, 0.75 " " left textcolor ls 0
}

plot  \
	[xmin:xmax] 1/0 notitle, \
	\
	1/0 with lines ls PLOT_STYLE3 title PLOT_TITLE3, \
	1/0 with lines ls PLOT_STYLE1 title PLOT_TITLE1, \
	\
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $11+$5}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):($2/1000000) with lines ls PLOT_STYLE1 lc rgb '#000000' notitle, \
	[ xmax - 14 * 86400 : xmax ] f(x) with lines ls PLOT_STYLE3 notitle
