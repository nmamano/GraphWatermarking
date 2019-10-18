
def massage_data(input_file, output_file):
    """ transforms the output of the 'group_data.sh' script to
    CSV format for plotting """
    with open(input_file, 'r') as fin:
        success_map = dict()
        disturbance_map = dict()
        network_set = set()
        prob_set = set()
        run_set = set()
        for line in fin:
            i = line.find("_0")
            network = line[:i]

            line = line[i+1:]
            i = line.find("_")
            prob = line[:i]

            line = line[i+1:]
            run = line[0]

            line = line[2:]
            values = line.split()

            success = values[3]

            disturbance = values[4]

            network_set.add(network)
            prob_set.add(prob)
            run_set.add(run)

            success_map[(network, prob, run)] = success
            disturbance_map[(network, prob, run)] = disturbance

        avg_success_map = dict()
        avg_disturbance_map = dict()
        for network in network_set:
            for prob in prob_set:
                success_total = 0
                disturbance_total = 0
                count = 0
                for run in run_set:
                    tup = (network, prob, run)
                    if tup in success_map:
                        success_total += float(success_map[tup])
                        disturbance_total += float(disturbance_map[tup])
                        count += 1
                avg_tup = (network, prob)
                if count == 0:
                    avg_success_map[avg_tup] = None
                    avg_disturbance_map[avg_tup] = None
                else:
                    avg_success_map[avg_tup] = success_total/count
                    avg_disturbance_map[avg_tup] = disturbance_total/count

    with open(output_file, 'w') as fout:
        headers = "probs"
        for network in network_set:
            headers += ","+network+"_success,"+network+"_disturbance"
        fout.write(headers+"\n")
        prob_list = list(prob_set)
        prob_list.sort()
        for prob in prob_list:
            prob_line = prob
            for network in network_set:
                avg_tup = (network, prob)
                success = avg_success_map[avg_tup]
                disturbance = avg_disturbance_map[avg_tup]
                if success is not None:
                    prob_line += ","+str(success)+","+str(disturbance)
                else:
                    prob_line += ",nan,nan"
            fout.write(prob_line+"\n")

input_file = "../experiments/data_2"
output_file = "../experiments/data_2.csv"
massage_data(input_file, output_file)
