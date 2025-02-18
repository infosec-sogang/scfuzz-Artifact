import sys, os
from common import init_elsc_bug_info
from common import collect_found_times
from common import EL, SC
from plot_ELSC_bug import analyze_dir, classify_targets

def print_median_time(bug_sig, targ_list, time_map_list, bug_info):
    iter_cnt = len(time_map_list)
    for targ in targ_list:
        found_times = collect_found_times(bug_sig, time_map_list, targ)
        found_times.sort()
        func_list = bug_info[targ]
        func_list = {func: [] for (sig, func) in func_list if bug_sig == sig and func is not None}
        for found_time in found_times:
            for (func, time) in found_time:
                if func not in func_list: func_list[func] = [time]
                else: func_list[func].append(time)
        
        for func in func_list:
            found_times = func_list[func]
            if len(found_times) <= iter_cnt/2:
                print("%s ( %s ) : N/A" % (targ, func))
            else:
                sec = ", ".join(map(str, found_times))
                print("%s ( %s ): %.2f" % (targ, func, found_times[iter_cnt//2]))

def main():
    if len(sys.argv) < 2:
        print("Usage: %s [result dir]" % sys.argv[0])
        exit(1)

    result_dir = sys.argv[1]
    bug_info = init_elsc_bug_info(SC, EL)
    targ_list = os.listdir(result_dir)
    iter_cnt = len(os.listdir(os.path.join(result_dir,targ_list[0])))
    targ_list.sort()

    time_map_list = []
    for iter in range(1, iter_cnt + 1):
        time_map = {}
        for target in targ_list:
            analyze_dir(bug_info, result_dir, target, iter, time_map)
        time_map_list.append(time_map)

    SC_list, EL_list = classify_targets(bug_info, targ_list)
    print_median_time(SC, SC_list, time_map_list)
    print("===================================")
    print_median_time(EL, EL_list, time_map_list)
    print("===================================")

if __name__ == "__main__":
    main()
