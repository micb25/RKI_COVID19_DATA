
CSV_SOURCE = "../RKI_COVID19_Impfquotenmonitoring.csv"

load "template.gnuplot"

set terminal png enhanced truecolor font "Liberation Sans,16" size 1600, 800 dl 2.0

set output "plot_vac_rel_overview.png"
set lmargin 25.0
set rmargin 5.0
set bmargin 5.0

set xlabel "geimpfter Bevölkerungsanteil (kumuliert)"
set format x '%4.1f%%'
set xrange [0: 1 < * < 100 ]
set yrange [1:16]
set style fill solid
unset key

bwidth = 0.8
set offsets 0,0,0.5-bwidth/2.0,0.5

set ytics ( \
	states[2]  16, states[3]  15, states[4]  14, states[5]  13, \
	states[6]  12, states[7]  11, states[8]  10, states[9]   9, states[10]  8, \
	states[11]  7, states[12]  6, states[13]  5, states[14]  4, states[15]  3, \
	states[16]  2, states[17]  1 \
)

population_cnt(x) = population[ x ]

set xtics 0, 0.5, 20 out nomirror rotate by 0 offset 0, 0 scale 1.2
set mxtics 2

# y-axis setup
unset ylabel
unset grid
set grid xtics ls 21 lc rgb '#aaaaaa'

set offsets graph 0.001, graph 0.20, graph 0.05, graph 0.05

plot \
     1/0 notitle, \
	"<awk -F, '{ if ((NR>1)&&($3>0)) print 17-$3, 100*$5 }' ../RKI_COVID19_Impfquotenmonitoring.csv | tail -n 16" using ($2/population_cnt(18-$1)):0:(0):($2/population_cnt(18-$1)):($1-bwidth/2.0):($1+bwidth/2.0):($1+1) with boxxyerror ls 1 notitle, \
	"<awk -F, '{ if ((NR>1)&&($3>0)) print 17-$3, 100*$5 }' ../RKI_COVID19_Impfquotenmonitoring.csv | tail -n 16" using ($2/population_cnt(18-$1)):($1):(sprintf("%.0f (%.2f%%)", $2/100, $2/population_cnt(18-$1))) with labels left offset graph 0.01, 0.0
