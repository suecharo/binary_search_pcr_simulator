#!/usr/bin/dev python
# coding: utf-8


from argparse import ArgumentError, ArgumentParser
import random
from copy import copy

DEFAULT_NUMS = {
    "simulate_num": 100,
    "block_size": 32,
    "sample_num": 256,
    "infected_rate": 0.3,
    "false_positive": 0.1,
    "false_negative": 0.1
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--simulate_num",
        default=DEFAULT_NUMS["simulate_num"],
        type=int,
        help=f"Simulate num (default: {DEFAULT_NUMS['simulate_num']})",
        metavar=""
    )
    parser.add_argument(
        "-b",
        "--block-size",
        default=DEFAULT_NUMS["block_size"],
        type=int,
        help=f"Block size (default: {DEFAULT_NUMS['block_size']})",
        metavar=""
    )
    parser.add_argument(
        "-s",
        "--sample-num",
        default=DEFAULT_NUMS["sample_num"],
        type=int,
        help=f"Number of sample (default: {DEFAULT_NUMS['sample_num']})",
        metavar=""
    ),
    parser.add_argument(
        "-i",
        "--infected-rate",
        default=DEFAULT_NUMS["infected_rate"],
        type=float,
        help="Rate of samples that are infected "
        f"(default: {DEFAULT_NUMS['infected_rate']})",
        metavar=""
    )
    parser.add_argument(
        "-fp",
        "--false-positive",
        default=DEFAULT_NUMS["false_positive"],
        type=float,
        help="False positive rate "
        f"(default: {DEFAULT_NUMS['false_positive']})",
        metavar=""
    )
    parser.add_argument(
        "-fn",
        "--false-negative",
        default=DEFAULT_NUMS["false_negative"],
        type=float,
        help="False negative rate "
        f"(default: {DEFAULT_NUMS['false_negative']})",
        metavar=""
    )

    args = parser.parse_args()

    return args


def validate_args(args):
    if args.simulate_num <= 0:
        raise ArgumentError(None, "Simulate num is greater than 1")
    if args.block_size <= 0:
        raise ArgumentError(None, "Block size is greater than 1")
    if args.sample_num <= 0:
        raise ArgumentError(None, "Sample num is greater than 1")
    if args.infected_rate < 0 or args.infected_rate > 1:
        raise ArgumentError(None, "Infected rate is 0 < rate < 1.")
    if args.false_positive < 0 or args.false_positive > 1:
        raise ArgumentError(None, "False positive rate is 0 < rate < 1.")
    if args.false_negative < 0 or args.false_negative > 1:
        raise ArgumentError(None, "False negative rate is 0 < rate < 1.")


def print_args(args):
    print(f"Simulate num:        {args.simulate_num}")
    print(f"Block size:          {args.block_size}")
    print(f"Sample num:          {args.sample_num}")
    print(f"Infected rate:       {args.infected_rate}")
    print(f"False positive rate: {args.false_positive}")
    print(f"False negative rate: {args.false_negative}")


def simulate(simulate_num,
             block_size,
             sample_num,
             infected_rate,
             false_positive,
             false_negative):
    result_counts = {
        "simulate_count": 0,
        "false_positive_count": 0,
        "false_negative_count": 0
    }
    for _ in range(simulate_num):
        samples = [1 if i < round(sample_num * infected_rate) else 0
                   for i in range(sample_num)]
        random.shuffle(samples)
        true_samples = copy(samples)
        simulated_samples = []

        samples = [samples[i:i+block_size]
                   for i in range(0, sample_num, block_size)]
        while len(samples) != 0:
            result_counts["simulate_count"] += 1
            block = samples.pop(0)
            if any(block):  # Positive
                if random.random() <= false_negative:
                    # As negative
                    for _ in range(len(block)):
                        simulated_samples.append(0)
                else:
                    # As positive
                    if len(block) != 1:
                        samples.insert(0, block[len(block) // 2:])
                        samples.insert(0, block[:len(block) // 2])
                    else:
                        simulated_samples.append(1)
            else:  # Negative
                if random.random() <= false_positive:
                    # As positive
                    if len(block) != 1:
                        samples.insert(0, block[len(block) // 2:])
                        samples.insert(0, block[:len(block) // 2])
                    else:
                        simulated_samples.append(1)
                else:
                    # As negative
                    for _ in range(len(block)):
                        simulated_samples.append(0)

        for i in range(sample_num):
            true_result = true_samples[i]
            simulated_result = simulated_samples[i]
            if true_result == 1 and simulated_result == 0:
                result_counts["false_negative_count"] += 1
            if true_result == 0 and simulated_result == 1:
                result_counts["false_positive_count"] += 1

    result = {
        "pcr_count": result_counts["simulate_count"] / simulate_num,
        "fp_rate":
        result_counts["false_positive_count"] / simulate_num / sample_num,
        "fn_rate":
        result_counts["false_negative_count"] / simulate_num / sample_num,
    }

    return result


def main():
    try:
        args = parse_args()
        validate_args(args)
        print_args(args)
        result = simulate(
            args.simulate_num,
            args.block_size,
            args.sample_num,
            args.infected_rate,
            args.false_positive,
            args.false_negative
        )
        print("-" * 40)
        print(f"Average number of times PCR: {result['pcr_count']}")
        print(
            f"Average binary search false positive rate: {result['fp_rate']}")
        print(
            f"Average binary search false negative rate: {result['fn_rate']}")
    except Exception:
        from traceback import print_exc
        from sys import exit
        print_exc()
        exit(1)


if __name__ == "__main__":
    main()
