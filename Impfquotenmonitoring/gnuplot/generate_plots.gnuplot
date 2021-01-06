
CSV_SOURCE = "../RKI_COVID19_Impfquotenmonitoring.csv"

load "template.gnuplot"

set xrange [xmin:xmax]
set xdata time
set timefmt "%s"
set format x "%d.%m.%y"

PLOT_TITLE = "Impfungen kumuliert"
PLOT_STYLE = 1
INDEX_COL = 5

do for [i=0:NUM_STATES-1] {
	output_name = sprintf("plot_vac_%i.png", i)
	set output output_name
	
	REGION_ID = sprintf("%i", i)
	REGION = states[i+1]
	
	load "plot_data.gnuplot"
}
