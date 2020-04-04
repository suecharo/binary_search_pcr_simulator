# Binary Search PCR Simulator

## How to use

```bash
>
python3 simulate.py --help
usage: simulate.py [-h] [--simulate-num] [-b] [-s] [-i] [-fp] [-fn]

optional arguments:
  -h, --help            show this help message and exit
  --simulate-num        Simulate num (default: 100)
  -b , --block-size     Block size (default: 32)
  -s , --sample-num     Number of sample (default: 256)
  -i , --infected-rate
                        Rate of samples that are infected (default: 0.3)
  -fp , --false-positive
                        False positive rate (default: 0.1)
  -fn , --false-negative
                        False negative rate (default: 0.1)

> python3 simulate.py
Simulate num:        100
Block size:          32
Sample num:          256
Infected rate:       0.3
False positive rate: 0.1
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 244.44
Average binary search false positive rate: 0.0148046875
Average binary search false negative rate: 0.13859375
```

## Result

- サンプル数と block size の関係
  - Block size が大きければ pcr の回数を減らせる

```bash
> python3 simulate.py --block-size 128
Simulate num:        100
Block size:          128
Sample num:          256
Infected rate:       0.3
False positive rate: 0.1
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 190.3
Average binary search false positive rate: 0.0108984375
Average binary search false negative rate: 0.1790234375

>python3 simulate.py --block-size 256 --sample-num 10000
Simulate num:        100
Block size:          256
Sample num:          10000
Infected rate:       0.3
False positive rate: 0.1
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 7077.7
Average binary search false positive rate: 0.010425
Average binary search false negative rate: 0.183598
```

- PCR の FP と binary search PCR の FP の関係
  - False Positive は普通にやるより下がる

```bash
> python3 simulate.py --block-size 256 --sample-num 10000 --fp 0.3
usage: simulate.py [-h] [--simulate-num] [-b] [-s] [-i] [-fp] [-fn]
simulate.py: error: unrecognized arguments: --fp 0.3
> python3 simulate.py --block-size 256 --sample-num 10000 -fp 0.3
Simulate num:        100
Block size:          256
Sample num:          10000
Infected rate:       0.3
False positive rate: 0.3
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 7521.18
Average binary search false positive rate: 0.040595
Average binary search false negative rate: 0.183343
```

- PCR の FN と binary search PCR の FN の関係
  - False Negative はあんまり変わらない
  - なんか知らんけど、PCR 回数は下がった

```bash
> python3 simulate.py --block-size 256 --sample-num 10000 -fn 0.3
Simulate num:        100
Block size:          256
Sample num:          10000
Infected rate:       0.3
False positive rate: 0.1
False negative rate: 0.3
----------------------------------------
Average number of times PCR: 1588.94
Average binary search false positive rate: 0.001471
Average binary search false negative rate: 0.287599
```

- 感染者が少ない場合 (パニックで適当な感じで人がたくさん来ている)
  - 結構いい感じ

```bash
> python3 simulate.py --block-size 256 --sample-num 10000 -i 0.05
Simulate num:        100
Block size:          256
Sample num:          10000
Infected rate:       0.05
False positive rate: 0.1
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 2665.64
Average binary search false positive rate: 0.0025039999999999997
Average binary search false negative rate: 0.030785000000000003
```

- 感染者が多い場合 (ちゃんと症状がある人が来ている)
  - あんまり良くない

```bash
> python3 simulate.py --block-size 256 --sample-num 10000 -i 0.8
Simulate num:        100
Block size:          256
Sample num:          10000
Infected rate:       0.8
False positive rate: 0.1
False negative rate: 0.1
----------------------------------------
Average number of times PCR: 9405.64
Average binary search false positive rate: 0.0069489999999999994
Average binary search false negative rate: 0.49246599999999996
```
