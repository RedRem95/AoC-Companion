# AoC-Companion

Simple AoC helper program you can use to develop your own solutions in python.
Simply install it in your python environment using pip from git.

## Usage

This is a simple usage example
```python

from AoC_Companion.AoC import AoC
from AoC_Companion.Day import Day, TaskResult, StarTask

class Day01(Day):
    
    def run_t1(self, data):
        return TaskResult(day=self, task=StarTask.Task01, result="Put your Result here", duration=0)
    
    def run_t2(self, data):
        return TaskResult(day=self, task=StarTask.Task02, result="Put your Result here", duration=0)

aoc = AoC(year=2021)
results = aoc.run_latest()
print(TaskResult.format(results=results))
```