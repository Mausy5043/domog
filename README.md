# domog
Platform independent domotica data grapher.


## Installing

```
sudo su -
cd /path/to/where/you/want/store/domog
git clone https://github.com/Mausy5043/domog.git
cd domog
./install.sh
./update.sh
```

## Execution
After installation the daemons start up automagically. Data stored in the MySQL database by the data gatherers of [domod](https://github.com/Mausy5043/domod.git) is retrieved and graphed. The graphs and the accompanying webpage are pushed to the [Grav-based](https://getgrav.org/) website.
This version queries the MySQL database in batches on every update. Graphs are made with `gnuplot`.

## Attribution
The python code for the daemons is based on previous work by
- [Charles Menguy](http://stackoverflow.com/questions/10217067/implementing-a-full-python-unix-style-daemon-process)
- [Sander Marechal](http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/)
