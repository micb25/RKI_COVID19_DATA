
CSV_SOURCE = "../RKI_COVID19_Impfquotenmonitoring.csv"

load "template.gnuplot"

set offsets 0.00, 0.00, graph 0.25, 0.00

set xrange [xmin:xmax]
set xdata time
set timefmt "%s"
set format x "%d.%m.%y"

set bmargin 4.25

PLOT_TITLE1 = "Erstimpfungen"
PLOT_TITLE2 = "Zweitimpfungen"
PLOT_STYLE1 = 1
PLOT_STYLE2 = 2

do for [i=0:NUM_STATES-1] {
	output_name = sprintf("plot_vac_%i.png", i)
	set output output_name
	
	REGION_ID = sprintf("%i", i)
	REGION = states[i+1]
	
	load "plot_data.gnuplot"
}
