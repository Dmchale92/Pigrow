#!/usr/bin/python
import os, sys
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
try:
    sys.path.append('/home/pi/Pigrow/scripts/')
    #sys.path.append('/home/pragmo/pigitgrow/Pigrow/scripts/')
    import pigrow_defs
    loc_locs = '/home/pi/Pigrow/config/dirlocs.txt'
    loc_dic = pigrow_defs.load_locs(loc_locs)
    graph_path = loc_dic['graph_path']
    self_log = loc_dic['self_log']
except:
    graph_path = './'
    self_log =  "./selflog.txt"

for argu in sys.argv[1:]:
    thearg = str(argu).split('=')[0]
    if  thearg == 'gp' or thearg == 'out':
        graph_path = str(argu).split('=')[1]
    elif thearg == 'log':
        self_log = str(argu).split('=')[1]
    elif thearg == '-h' or thearg == '--help':
        print(" selflog_graph maker;")
        print("  gp=PATH    = PATH to save graphs to e,g, /home/pi/Pigrow/graphs/ ")
        print(" log=PATH    = PATH to self_log to e,g, /home/pi/Pigrow/logs/selflog.txt ")
log_dic = {}    # Reused for every line of the log file
                     ## Lists used to make graphs.
dates = []      # Used for all the graphs
cpu_a1 = []    #
cpu_a5 = []    #  cpu load average for one min, five min, fifteen min
cpu_a15 = []   #
mem_a = []      #
mem_f = []      #  mem avail, full, total
mem_t = []      #
disk_p = []    #
disk_f = []    #  Disk Percent, Full, total, used
disk_t = []    #
disk_u = []    #
up = []         # uptime

with open(self_log, "r") as f:
    print self_log
    for line in f:
        try:
            line = line.split('>')
            for item in line:
                item = item.split("=")
                if len(item) == 1:
                    break
                name = item[0].strip()
                value = item[1].strip()
                log_dic[name]=value
        #time and date
            date = log_dic['timenow'].split('.')[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            dates.append(date)
        #CPU LOAD AVE
            load_ave1 = log_dic['load_ave1']
            load_ave5 = log_dic['load_ave5']
            load_ave15 = log_dic['load_ave15']
            cpu_a1.append(load_ave1)
            cpu_a5.append(load_ave5)
            cpu_a15.append(load_ave15)
        #mem space
            mem_avail = int(log_dic['memavail'].split(" ")[0])/1024
            mem_free = int(log_dic['memfree'].split(" ")[0])/1024
            mem_total = int(log_dic['memtotal'].split(" ")[0])/1024
            mem_a.append(mem_avail)
            mem_f.append(mem_free)
            mem_t.append(mem_total)
        #Disk fullness
            disk_percent = log_dic['disk_percent']
            disk_free = int(log_dic['disk_free'])/1024/1024
            disk_total = int(log_dic['disk_total'])/1024/1024
            disk_used = int(log_dic['disk_used'])/1024/1024
            disk_p.append(disk_percent)
            disk_f.append(disk_free)
            disk_t.append(disk_total)
            disk_u.append(disk_used)
        #uptime
            uptime = log_dic['uptime_sec']
            up.append(uptime)
        except:
            print("didn't parse" + str(item))
            #raise

#
#  Code for making the graphs.
#

def make_cpu_graph(dates, cpu_a1, cpu_a5, cpu_a15):
    print("Attempting to make cpu graph")
    fig, ax = plt.subplots(3, sharex=True)
    ax[0].plot_date(dates, cpu_a1)
    ax[1].plot_date(dates, cpu_a5)
    ax[2].plot_date(dates, cpu_a15)
    ax[0].plot(dates, cpu_a1)
    ax[1].plot(dates, cpu_a5)
    ax[2].plot(dates, cpu_a15)
    ax[0].set_title("CPU Load from " + str(dates[0].strftime("%b-%d %H:%M")) + " to " + str(dates[-1].strftime("%b-%d %H:%M")) + " UTC")
    #plt.subplots(2, 2)
    fig.autofmt_xdate()
    plt.savefig(graph_path + "Selflog_cpu_graph.png")

def make_mem_graph(dates, mem_a, mem_f, mem_t):
    print("Attempting to make mem useage graoh")
    fig2, ax2 = plt.subplots()
    ax2.plot_date(dates, mem_a, '-', color='green')
    ax2.plot_date(dates, mem_f, '-', color='blue')
    ax2.plot_date(dates, mem_t, '-', color='black')
    ax2.set_title("Memory Use from " + str(dates[0].strftime("%b-%d %H:%M")) + " to " + str(dates[-1].strftime("%b-%d %H:%M")) + " UTC")
    plt.ylabel("Memory in MB")
    fig2.autofmt_xdate()
    plt.savefig(graph_path + "Selflog_mem_graph.png")
    #plt.show()

def make_disk_graphs(dates, disk_p, disk_f, disk_t, disk_u):
    print("Attempting to make disk useage graoh")
    #fig3, ax3 = plt.subplots()
    fig3, ax3 = plt.subplots(2, sharex=True)
    plt.ylabel("Disk Memory in MB")
    ax3[0].plot_date(dates, disk_t, '-', color='black')
    ax3[0].plot_date(dates, disk_f, '-', color='green')
    ax3[0].plot_date(dates, disk_u, '-', color='red')
    ax3[0].set_title("Disk Use from " + str(dates[0].strftime("%b-%d %H:%M")) + " to " + str(dates[-1].strftime("%b-%d %H:%M")) + " UTC")
    ax3[1].plot_date(dates, disk_p, '-')
    ax3[1].set_title("Percentage of disk used")
    fig3.autofmt_xdate()
    plt.savefig(graph_path + "Selflog_disk_graph.png")

def make_graph_up(dates, up):
    print("Attempting to make disk useage graoh")
    fig4, ax4 = plt.subplots()
    ax4.plot(dates, up, '-')
    ax4.set_title("Uptime; " + str(dates[0].strftime("%b-%d %H:%M")) + " to " + str(dates[-1].strftime("%b-%d %H:%M")) + " UTC")
    fig4.autofmt_xdate()
    plt.savefig(graph_path + "Selflog_up_graph.png")



if __name__ == '__main__':
    print "Last log was " + str(datetime.datetime.now() - date).split('.')[0] + " ago"
    print "there are " + str(len(cpu_a1)) + " data points for graphhs"
    make_cpu_graph(dates, cpu_a1, cpu_a5, cpu_a15)
    make_mem_graph(dates, mem_a, mem_f, mem_t)
    make_disk_graphs(dates, disk_p, disk_f, disk_t, disk_u)
    make_graph_up(dates, up)

#plt.show()
#print date
#print len(dates)

###
##  This is for listing the things in the log.
#

#for key,value in log_dic.iteritems():
#    num_of_s = 40 - len(key)
#    spaces = str(key)
#    for x in range(0,num_of_s):
#        spaces += " "
#    print spaces + " == " + str(value)
#print log_dic
