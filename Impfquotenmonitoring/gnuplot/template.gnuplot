set terminal png enhanced truecolor font "Liberation Sans,16" size 800, 600 dl 2.0 
set encoding utf8
set minussign

set fit quiet logfile '/dev/null'
set fit errorvariables

# margins
set lmargin 9.60
set rmargin 1.45
set tmargin 0.75
set bmargin 5.75

# colors and plot style
set style line  1 lc rgb '#0000FF' lt 1 lw 3 pt 7 ps 1.50 
set style line  2 lc rgb '#830683' lt 1 lw 3 pt 7 ps 1.50 
set style line  3 lc rgb '#5c5c5c' lt 1 lw 3 pt 7 ps 1.50
set style line  4 lc rgb '#006000' lt 1 lw 3 pt 7 ps 1.50 
set style line  5 lc rgb '#006000' lt 1 lw 3 pt 7 ps 1.50
set style line  6 lc rgb '#e6daa6' lt 1 lw 1 pt 7 ps 1.50 dt "."
set style line  7 lc rgb '#3f9b0b' lt 1 lw 3 pt 7 ps 1.50
set style line  8 lc rgb '#ff8a1e' lt 1 lw 3 pt 7 ps 1.50
set style line  9 lc rgb '#ff0000' lt 1 lw 3 pt 7 ps 1.50
set style line  10 lc rgb '#000000' lw 1 lt 1 dt "  .  "
set style line  11 lc rgb '#aaaaaa' lw 1 lt 1 dt "  .  "
set style line  12 lc rgb '#FF0000' lw 1.5
set style line  13 lc rgb '#FF0000' lw 1.5 dt "."
set style line  16 lc rgb '#800080' lt 1 lw 2
set style line  17 lc rgb '#FF0000' lt 1 lw 2
set style line  18 lc rgb '#ff8a1e' lt 1 lw 2
set style line  19 lc rgb '#5c5c5c' lt 1 lw 2
set style line  21 dt 3
set style line  31 lc rgb '#0000FF' lt 1 lw 1 pt 7 ps 1.50
set style line  32 lc rgb '#0000A0' lt 1 lw 1 pt 7 ps 1.50
set style line  33 lc rgb '#A000A0' lt 1 lw 1 pt 7 ps 1.50
set style line  34 lc rgb '#600060' lt 1 lw 1 pt 7 ps 1.50

# arrow
set style line  40 lc rgb '#30808080'

# grid
set grid xtics ls 21 lc rgb '#aaaaaa'
set grid ytics ls 21 lc rgb '#aaaaaa'

# misc
set samples 30
set style increment default
set style fill transparent solid 0.20 border
# set datafile separator ","

# axes
set xtics 1*86400 out nomirror rotate by 90 offset 0, -4.1 scale 1.2
set mxtics 1

# y-axis setup
unset ylabel

set format y '%8.0f'
set ytics out nomirror scale 1.2
set mytics 2

set key opaque
set border back

# filter negative values
filter_neg(x)=(x>=0)?(x):(1/0)

ONE_DAY_IN_MS = 86400000
ONE_DAY_IN_S = ONE_DAY_IN_MS / 1000

set offsets 0.00, 0.00, graph 0.15, 0.00

# key
set key at graph 0.02, 0.98 left top invert spacing 1.5 box ls 3 opaque

# states
NUM_STATES = 17
array states[NUM_STATES]

states[1] = "Deutschland"
states[2] = "Schleswig-Holstein"
states[3] = "Hamburg"
states[4] = "Niedersachsen"
states[5] = "Bremen"
states[6] = "Nordrhein-Westfalen"
states[7] = "Hessen"
states[8] = "Rheinland-Pfalz"
states[9] = "Baden-Württemberg"
states[10] = "Bayern"
states[11] = "Saarland"
states[12] = "Berlin"
states[13] = "Brandenburg"
states[14] = "Mecklenburg-Vorpommern"
states[15] = "Sachsen"
states[16] = "Sachsen-Anhalt"
states[17] = "Thüringen"

# stats for x
stats "../RKI_COVID19_Impfquotenmonitoring.csv" using 1 nooutput
xmin = int(STATS_min)
xmax = int(STATS_max)

# latest update
update_str = "{/*1.00 Datenquelle: Robert Koch-Institut; letzte Aktualisierung: " . system("date +%d.%m.%Y") . "}"

set xrange [xmin:xmax]
set xdata time
set timefmt "%s"
set format x "%d.%m.%y"
