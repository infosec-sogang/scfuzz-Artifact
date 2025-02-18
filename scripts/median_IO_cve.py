import sys, os
from common import init_io_cve_info, print_median_time
from common import IB
from plot_IO_cve import analyze_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: %s [result dir]" % sys.argv[0])
        exit(1)

    result_dir = sys.argv[1]
    cve_info = init_io_cve_info(IB)
    targ_list = os.listdir(result_dir)
    iter_cnt = len(os.listdir(os.path.join(result_dir,targ_list[0])))
    targ_list.sort()

    time_map_list = []
    for iter in range(1, iter_cnt + 1):
        time_map = {}
        for target in targ_list:
            analyze_dir(cve_info, result_dir, target, iter, time_map)
        time_map_list.append(time_map)

    print_median_time(IB, targ_list, time_map_list)

if __name__ == "__main__":
    main()