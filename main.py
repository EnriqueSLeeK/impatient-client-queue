
from json import load

def main(config: dict, result: dict):
    print(config)
    return

if __name__ == "__main__":
    config = {}

    result = {
        "N_res": [],
        "W_mean": [],
        "W_cis": [],
        "TM_means": [],
        "TM_cis": [],
        "W_values": [],
        "TM_values": []
    }

    with open("config.json") as f:
        config = load(f)
    main(config)
