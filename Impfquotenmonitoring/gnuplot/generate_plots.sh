#!/bin/bash

gnuplot generate_plots.gnuplot > /dev/null
gnuplot generate_plots_rel.gnuplot > /dev/null
gnuplot generate_plots_rel_2nd.gnuplot > /dev/null
gnuplot generate_plots_combined.gnuplot > /dev/null
gnuplot generate_plot_overview.gnuplot > /dev/null
gnuplot generate_plot_overview_2nd_vac.gnuplot > /dev/null
