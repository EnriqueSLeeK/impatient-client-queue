
import json
import numpy as np

# Calculation Functions
def not_served_proportion(served, forfeit, queue_len):
    return (forfeit / (served + forfeit + queue_len))

def prob_forfeit(queue_len, cashier_quant):
    return queue_len / (queue_len + cashier_quant)

def std_error(variance, number_experiment):
    return variance / np.sqrt(number_experiment)

def calculate_confidence_interval(std_error):
    return 2 * 1.96 * std_error

# Simulation
def simulate_one_instance(config: dict):

    time = 0
    forfeit = 0
    # No one was served
    served = 0
    proportion = -1
    waiting_max = -1

    queue = []
    curr_queue_size = 0
    total_joined_queue = 0

    cashier = [0 for _ in range(config['n'])]

    while (True):
        # Arrival interval
        arrival_interval = np.random.exponential(1 / config['lambda'])
        time += arrival_interval

        # Check to return
        if (time > config['T']):
            return {
                'served': served,
                'forfeit': forfeit,
                'proportion': proportion,
                'waiting_max': waiting_max
            }

        total_joined_queue += 1
        queue.append(time)

        lowest_cashier_time_index = np.argmin(cashier)

        # Serving
        while (cashier[lowest_cashier_time_index] <= time and
                served < total_joined_queue):


            serving_interval = np.random.exponential(1 / config['mu'])

            cashier[lowest_cashier_time_index] = np.max([cashier[lowest_cashier_time_index],
                                                        queue[served]]) + serving_interval
            waiting_max = np.max([waiting_max,
                                 np.abs(cashier[lowest_cashier_time_index] - queue[served])])
            served += 1
            lowest_cashier_time_index = np.argmin(cashier)

        curr_queue_size = np.max([0, (total_joined_queue - 1) - served])

        # Check if the client left without joining
        client_forfeit = np.random.binomial(n=1, p=prob_forfeit(queue_len=curr_queue_size,
                                                                cashier_quant=config['n']))
        if (client_forfeit == 1):
            total_joined_queue -= 1
            forfeit += 1
            queue.pop()

        # Calculate the current queue size
        curr_queue_size = total_joined_queue - served
        proportion = not_served_proportion(served=served,
                                           forfeit=forfeit,
                                           queue_len=curr_queue_size)

# Wrapper to append a element to an array
def add_elem(target_array, data):
    target_array.append(data)

def main(config: dict):

    served_list = []
    forfeit_list = []
    proportion_list = []
    waiting_max_list = []
    confidence_interval = 1
    repeat_counter = 0

    partial_mean_proportion_list = []
    partial_mean_waiting_max_list = []

    while (confidence_interval >= config['se_threshold']):
        repeat_counter += 1
        for _ in range(config['N']):
            simulation_result = simulate_one_instance(config)
            add_elem(served_list, simulation_result['served'])
            add_elem(forfeit_list, simulation_result['forfeit'])
            add_elem(proportion_list, simulation_result['proportion'])
            add_elem(waiting_max_list, simulation_result['waiting_max'])

        std_error_value = std_error(np.std(proportion_list), config['N'])
        confidence_interval = calculate_confidence_interval(std_error_value)
        add_elem(partial_mean_proportion_list, np.mean(proportion_list))
        add_elem(partial_mean_waiting_max_list, np.mean(waiting_max_list))


if __name__ == '__main__':
    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)
    main(config)
