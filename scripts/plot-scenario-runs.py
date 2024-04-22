import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

# Assuming your data is in the following format:
# [test_no, value1, value2, value3]
data = [
    [1, 2, 2, 2],
    [2, 45.38986799889244, 80.90140990061627, 120.37419930002216],
    [3, 8.045872500315454, 12.003339599687024, 10.733222799899522],
    [4, 319.9650784003097, 635.5689940010052, 637.6496478002082],
    [5, 6.849676198544332, 36.86405830230797, 35.08654409961309],
    [6, 736.8222681998304, 736.1272995989566, 747.6204743998096],
    [7, 762.3605406992283, 729.1856137017021, 783.2845127002656],
    [8, 802.0422464000148, 800.3269172990258, 798.1906367989723]
]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the data points as dots
for test_no, value1, value2, value3 in data:
    ax.scatter(test_no, value1, color='r', marker='o', label='Run 1')
    ax.scatter(test_no, value2, color='g', marker='o', label='Run 2')
    ax.scatter(test_no, value3, color='b', marker='o', label='Run 3')

# Set the x-axis labels
ax.set_xticks(range(1, len(data) + 1))
ax.set_xticklabels([str(test_no) for test_no in range(1, len(data) + 1)])

# Set the y-axis label
ax.set_ylabel('Service time (ms)')
ax.set_xlabel('Scenarios')

# Rotate the x-axis labels
plt.xticks(rotation=45)

# Plot the data points as dots
value1_dots = ax.scatter([], [], color='r', marker='o', label='Run 1')
value2_dots = ax.scatter([], [], color='g', marker='o', label='Run 2')
value3_dots = ax.scatter([], [], color='b', marker='o', label='Run 3')
# Add a legend
ax.legend(handles=[value1_dots, value2_dots, value3_dots])

# Add a title
plt.title('Asc Sort With After Timestamp Query', fontsize=16)

# Show the plot
plt.show()