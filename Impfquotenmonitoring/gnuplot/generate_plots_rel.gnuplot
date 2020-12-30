
CSV_SOURCE = "../RKI_COVID19_Impfquotenmonitoring.csv"

load "template.gnuplot"

set lmargin 12.60

PLOT_TITLE = "Impfungen kumulativ"
PLOT_STYLE = 1
INDEX_COL = 5

do for [i=0:NUM_STATES-1] {
	output_name = sprintf("plot_vac_rel_%i.png", i)
	set output output_name
	
	REGION_ID = sprintf("%i", i)
	REGION = states[i+1]
	POPULATION = population[i+1]
	
	load "plot_data_rel.gnuplot"
}
