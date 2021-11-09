# Tower of Hanoi - A Basic Implementation
A basic tool for solving the problem known as Tower of Hanoi. The problem is defined as follows. We are given n disks, each of a unique radius/size, and three rods called "source", "auxiliary", and "target". Initially, all disks are stacked on the source rod and they are sorted by their radius: the largest disk is at the bottom of the rod and the smallest one is at the top of the rod. The goal is to move all the disks to the target rod. Moreover, one has to comply with the following two rules: 
1) only one disk can be moved at a time, and
2) a disk cannot be put on a smaller disk (i.e., disks on a rod are always sorted by their size). 

## Installation
You just need to have Python 3 installed to run the tool. 

## Running the Tool
```
python3 ./toh.py -n <k>
```
where `<k>` is the number of disks, e.g., ``python3 ./toh.py -n 3``. The expected output should look as follows:
```
To move all disks from the source to the target disk, perform the following 7 step(s) (one disk per step):
rod1 --> rod3
rod1 --> rod2
rod3 --> rod2
rod1 --> rod3
rod2 --> rod1
rod2 --> rod3
rod1 --> rod3
```

The tool implements two algorithms for computing the movement instructions; a recursive one and an iterative one. You can specify the algorithm to be used via the flag `--algorithm <alg>`, where `<alg>` is either `recursive` or `iterative`. Moreover, via the flags `--source`, `--target`, and `--aux`, you can customize the names/labels of the source, target, and auxiliary rods, respectively. Run `python3 --help` to see all available options. 

## Copyright Note
This (toy) tool has been developed by Jaroslav Bendik and it is distributed under the GPL-3.0 License (see the LICENSE file).

The tool is publicly available on github: https://github.com/jar-ben/tower-of-hanoi
