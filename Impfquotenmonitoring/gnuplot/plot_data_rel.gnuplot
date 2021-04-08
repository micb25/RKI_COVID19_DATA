
# x-axis setup
set ylabel "Bevölkerungsanteil"
set format y '%2.0f%%'
set yrange [0: 0.1 < * < 100]

set label 1  at graph 0.99, 0.95 sprintf("{/:Bold %s}", REGION) right textcolor ls 10
set label 2  at graph 0.99, 0.89 update_str font ",12" right textcolor ls 10

# fit
m = 1
n = -STATS_min
f(x) = m * x + n
fit [ xmax - 14 * 86400 : xmax ] f(x) "<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $5}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):(100*$2/POPULATION) via m, n

vac_per_day_rel = m * 86400
vac_per_day = vac_per_day_rel * POPULATION / 100.0

set label 6 at graph 0.03, 0.75 " " left textcolor ls 0
set label 7 at graph 0.03, 0.75 " " left textcolor ls 0
set label 8 at graph 0.03, 0.75 " " left textcolor ls 0

if ( vac_per_day_rel > 0 ) {
	set label 3 at graph 0.03, 0.71 "{/:Bold 14-Tage-Trend (Erstimpfungen):}" left textcolor ls 10
	set label 4 at graph 0.06, 0.64 sprintf("%+.0f Impfungen pro Tag", vac_per_day) left textcolor ls 10
	set label 5 at graph 0.06, 0.57 sprintf("%+.2f%% geimpfter Anteil pro Tag", vac_per_day_rel) left textcolor ls 10

	line = 0.50
	achievement_25 = (25 - f(STATS_max) ) / vac_per_day_rel
	achievement_50 = (50 - f(STATS_max) ) / vac_per_day_rel
	achievement_75 = (75 - f(STATS_max) ) / vac_per_day_rel
	
	if ( achievement_25 > 0 ) {
		set label 6 at graph 0.06, line sprintf("25%% erreicht in %.0f Tagen", achievement_25) left textcolor ls 10
		line = line - 0.07
	}
	if ( achievement_50 > 0 ) {
		set label 7 at graph 0.06, line sprintf("50%% erreicht in %.0f Tagen", achievement_50) left textcolor ls 10
		line = line - 0.07
	}
	if ( achievement_75 > 0 ) {
		set label 8 at graph 0.06, line sprintf("75%% erreicht in %.0f Tagen", achievement_75) left textcolor ls 10
		line = line - 0.07
	}
} else {
	set label 3 at graph 0.03, 0.75 " " left textcolor ls 0
	set label 4 at graph 0.03, 0.75 " " left textcolor ls 0
	set label 5 at graph 0.03, 0.75 " " left textcolor ls 0
}

plot  \
	[xmin:xmax] 1/0 notitle, \
	\
	1/0 with lines ls PLOT_STYLE3 title PLOT_TITLE3, \
	1/0 with lines ls PLOT_STYLE2 title PLOT_TITLE2, \
	1/0 with lines ls PLOT_STYLE1 title PLOT_TITLE1, \
	\
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $5}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):(100*$2/POPULATION) with lines ls PLOT_STYLE1 notitle, \
	"<awk -F, '{ if ((NR>1)&&($3==".REGION_ID.")) print $1, $11}' ../RKI_COVID19_Impfquotenmonitoring.csv" using ($1):(100*$2/POPULATION) with lines ls PLOT_STYLE2 notitle, \
	[ xmax - 14 * 86400 : xmax ] f(x) with lines ls PLOT_STYLE3 notitle
