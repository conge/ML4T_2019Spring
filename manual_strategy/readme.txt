0. List of files needed for the project to run

    indicators.py
    TheoreticallyOptimalStrategy.py
    ManualStrategy.py
    marketsimcode.py

---------------------

1. indicators.py

1.1 Run the code
PYTHONPATH=..:. python indicators.py

1.2: Output
Running the code in indicators.py will generate three png images:
 01_Price_over_SMA_ratio.png
 02_bb_indicator.png
 03_momentum.png
These images are used in the report (Report.PDF) as figure 1, figure 2 and figure 3.


2. TheoreticallyOptimalStrategy.py

2.1 Run the code
PYTHONPATH=..:. python TheoreticallyOptimalStrategy.py

2.2 Output

Running the code TheoreticallyOptimalStrategy.py will generate 1 image named "04_TOS.png". It will be saved in the same
directory where the .py file. The image is used in Report.PDF as figure 4.
Performance results of the strategy and the benchmark will be shown on display.

3. ManualStrategy.py

3.1 Run the code

PYTHONPATH=..:. python ManualStrategy.py

3.2 Out put

Running the code ManualStrategy.py will generate 2 images named "05_MS_insample.png" and "06_MS_OutSample.png".
It will be saved in the same directory where the .py file. The images are used in Report.PDF as figure 5 and figure 6.
Performance results of the strategy and the benchmark will be shown on display. The performance results of the strategy on
in sample and out sample analysis were displayed on console.


Note: The packages/code below are also needed to run the codes above successfully.

numpy
pandas
datetime
matplotlib.pyplot
util.py
