#!/usr/bin/env gnuplot

# graph of humidity (and temperature)

# datafile
ifnameh = "/tmp/domog/mysql/sql22h.csv"
ifnamed = "/tmp/domog/mysql/sql22d.csv"
ifnamew = "/tmp/domog/mysql/sql22w.csv"
set output ofname = "/tmp/domog/site/img/day22.png"

# ******************************************************* General settings *****
set terminal png truecolor enhanced font "Vera" 9 size 1280,320
set datafile separator ';'
set datafile missing "NaN"    # Ignore missing values
set grid
tz_offset = utc_offset / 3600 # GNUplot only works with UTC. Need to compensate
                              # for timezone ourselves.
# Positions of split between graphs
LMARG = 0.056
LMPOS = 0.403
MRPOS = 0.75
RMARG = 0.96

min(x,y) = (x < y) ? x : y
max(x,y) = (x > y) ? x : y

# ********************************************************* Statistics (R) *****
# stats to be calculated here of column 2 (UX-epoch)
stats ifnameh using 2 name "X" nooutput

Xh_min = X_min + utc_offset - 946684800
Xh_max = X_max + utc_offset - 946684800

# stats to be calculated here for Y-axes
stats ifnameh using 3 name "Yh" nooutput

# stats for Y2-axis
stats ifnameh using 4 name "Y2h" nooutput

# ********************************************************* Statistics (M) *****
# stats to be calculated here of column 2 (UX-epoch)
stats ifnamed using 2 name "X" nooutput

Xd_min = X_min + utc_offset - 946684800
Xd_max = X_max + utc_offset - 946684800

# stats to be calculated here for Y-axes
stats ifnamed using 3 name "Yd" nooutput

# stats for Y2-axis
stats ifnamed using 4 name "Y2d" nooutput

# ********************************************************* Statistics (L) *****
# stats to be calculated here of column 2 (UX-epoch)
stats ifnamew using 2 name "X" nooutput
Xw_min = X_min + utc_offset - 946684800
Xw_max = X_max + utc_offset - 946684800

# stats for Y-axis
stats ifnamew using 3 name "Yw" nooutput

# stats for Y2-axis
stats ifnamew using 4 name "Y2w" nooutput

Ymax = max(max(Yd_max, Yh_max), Yw_max) +1
Ymin = min(min(Yd_min, Yh_min), Yw_min) -1
Y2max = max(max(Y2d_max, Y2h_max), Y2w_max) +1
Y2min = min(min(Y2d_min, Y2h_min), Y2w_min) -1

set multiplot layout 1, 3 title "Humidity \\& Temperature (DHT22) ".strftime("( %Y-%m-%dT%H:%M:%S )", time(0)+utc_offset)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                                       LEFT PLOT: past week
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ***************************************************************** X-axis *****
set xlabel "past week"       # X-axis label
set xdata time               # Data on X-axis should be interpreted as time
set timefmt "%s"             # Time in log-file is given in Unix format
set format x "%a %d"            # Display time in 24 hour notation on the X axis
set xrange [ Xw_min : Xw_max ]

# ***************************************************************** Y-axis *****
set ylabel "Humidity [%]"
set yrange [ Ymin : Ymax ]

# **************************************************************** Y2-axis *****
set y2label " "
set y2tics format " "
set y2range [ Y2min : Y2max ]

# ***************************************************************** Legend *****
set key inside top left horizontal box
set key samplen 1
set key reverse Left

# ***************************************************************** Output *****
set arrow from graph 0,graph 0 to graph 0,graph 1 nohead lc rgb "#cc0000bb" front
# set arrow from graph 1,graph 0 to graph 1,graph 1 nohead lc rgb "green" front
#set object 1 rect from screen 0,0 to screen 1,1 behind
#set object 1 rect fc rgb "#eeeeee" fillstyle solid 1.0 noborder
#set object 2 rect from graph 0,0 to graph 1,1 behind
#set object 2 rect fc rgb "#ffffff" fillstyle solid 1.0 noborder

set lmargin at screen LMARG
set rmargin at screen LMPOS

# ***** PLOT *****
plot ifnamew \
      using ($2+utc_offset):4 title " Temperature [degC]" axes x1y2  with points pt 5 ps 0.2 fc rgb "#ccbb0000" \
  ,'' using ($2+utc_offset):3 title " Humidity [%]"      with points pt 5 ps 0.2 fc rgb "#cc0000bb" \



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                                     MIDDLE PLOT:  past day
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ***************************************************************** X-axis *****
set xlabel "past day"       # X-axis label
set xdata time               # Data on X-axis should be interpreted as time
set timefmt "%s"             # Time in log-file is given in Unix format
set format x "%R"            # Display time in 24 hour notation on the X axis
set xrange [ Xd_min : Xd_max ]

# ***************************************************************** Y-axis *****
set ylabel " "
set ytics format " "
set yrange [ Ymin : Ymax ]

# **************************************************************** Y2-axis *****
set y2label " "
set y2tics format " "
set y2range [ Y2min : Y2max ]

# ***************************************************************** Legend *****
unset key

# ***************************************************************** Output *****
set arrow from graph 0,graph 0 to graph 0,graph 1 nohead lc rgb "black" front
set lmargin at screen LMPOS+0.001
set rmargin at screen MRPOS

# ***** PLOT *****
plot ifnamed \
      using ($2+utc_offset):4 axes x1y2 with points pt 5 ps 0.2 fc rgb "#ccbb0000" \
  ,'' using ($2+utc_offset):3 with points pt 5 ps 0.2 fc rgb "#cc0000bb" \

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                                      RIGHT PLOT: past hour
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ***************************************************************** X-axis *****
set xlabel "past hour"       # X-axis label
set xdata time               # Data on X-axis should be interpreted as time
set timefmt "%s"             # Time in log-file is given in Unix format
set format x "%R"            # Display time in 24 hour notation on the X axis
set xrange [ Xh_min : Xh_max ]
set xtics textcolor rgb "red"

# ***************************************************************** Y-axis *****
set ylabel " "
set ytics format " "
set yrange [ Ymin : Ymax ]

# **************************************************************** Y2-axis *****
set y2label "Temperature [degC]"
set y2tics format "%.0f"
set y2range [ Y2min : Y2max ]
set y2tics border

# ***************************************************************** Legend *****
unset key

# ***************************************************************** Output *****
set arrow from graph 1,graph 0 to graph 1,graph 1 nohead lc rgb "#ccbb0000" front
set lmargin at screen MRPOS+0.001
set rmargin at screen RMARG

# ***** PLOT *****
plot ifnameh \
      using ($2+utc_offset):4 axes x1y2 with points pt 5 ps 0.2 fc rgb "#ccbb0000" \
  ,'' using ($2+utc_offset):3 with points pt 5 ps 0.2 fc rgb "#cc0000bb" \

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                                                 FINALIZING
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

unset multiplot
