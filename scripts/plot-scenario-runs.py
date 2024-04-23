import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

# Assuming your data is in the following format:
# [test_no, value1, value2, value3]
# Desc Sort Size
data = [
    [1, 2, 2, 2],
    [2, 3.4950084998854436, 3.3130618992800014, 3.1608804007191793],
    [3, 3.739076100191596, 3.54519229986181, 4.3179377003980335],
    [4, 3.2623993995002825, 3.454105198761681, 3.0559134982468095],
    [5, 3.0176207998010796, 2.9318905013496988, 2.139642898691818],
    [6, 4.41621059908357, 2.853143802349223, 3.6186473993438995],
    [7, 3.755997100233799, 3.8341159026458627, 3.2316381017153617],
    [8, 4.2387181987578515, 2.375556702099857, 2.9355329013924347]
]
# Asc Sort Size
# data = [
#     [1, 2, 2, 2],
#     [2, 2.219128999786335, 2.4799346008876455, 1.7827261008278583],
#     [3, 3.392400900520443, 2.421962000153144, 1.7315654000412906],
#     [4, 1.9423050987825263, 2.204024502862012, 1.403117099107476],
#     [5, 3.6187159996188716, 1.4647050040366594, 1.5592491981806234],
#     [6, 2.985163098855992, 2.022620900606853, 2.1029225987149402],
#     [7, 2.2159603988257004, 1.8035060002148384, 1.8506682990846457],
#     [8, 3.35270219911763, 2.8374186003929935, 1.5650557001208654]
# ]
# Desc Sort Timestamp
# data = [
#     [1, 2, 2, 2],
#     [2, 18.16768450098607, 36.21833349970984, 51.82455749982182],
#     [3, 25.412215599772026, 55.09891879901261, 90.40329919698706],
#     [4, 54.89094789918454, 19.61056699983601, 53.46505340021395],
#     [5, 18.30694399868662, 57.12241860164795, 14.503174299170496],
#     [6, 60.047730300357216, 16.01014269690495, 51.380955597778666],
#     [7, 28.29639200317615, 52.847977001874824, 6.995748100962373],
#     [8, 31.611817999873892, 14.579896499708411, 52.68458249884134]
# ]
# Asc Sort Timestamp
# data = [
#     [1, 2, 2, 2],
#     [2, 3.036338900892588, 2.91309669992188, 2.979032399161952],
#     [3, 25.61910260001241, 447.19449849999364, 436.6056398015644],
#     [4, 3.007383598560409, 313.4067156981473, 313.7806795999495],
#     [5, 1.7715052996209126, 159.42069550146698, 158.27666459808825],
#     [6, 1.922272200317821, 2.809564399285591, 2.973678000125801],
#     [7, 2.962619000390987, 2.955147797547397, 1.5955369006405817],
#     [8, 2.9503099001885857, 1.6674499005603138, 2.54157389899774]
# ]
# Desc Sort With After Timestamp Query
# data = [
#     [1, 2, 2, 2],
#     [2, 657.8682727007617, 297.8924642002312, 691.241214299771],
#     [3, 542.1588163000706, 343.7583888999143, 473.9234483000473],
#     [4, 298.09097979978105, 754.9685960995703, 779.6476259984047],
#     [5, 517.7298767001048, 68.11747180181555, 67.28579180344241],
#     [6, 1032.890935098476, 1020.7852725030534, 1020.6153883995285],
#     [7, 1075.543434699648, 1018.7951933003205, 1073.847387598289],
#     [8, 1084.2060713992396, 1094.1826961006882, 1100.8044121019338]
# ]
# Asc Sort With After Timestamp Query
# data = [
#     [1, 2, 2, 2],
#     [2, 45.38986799889244, 80.90140990061627, 120.37419930002216],
#     [3, 8.045872500315454, 12.003339599687024, 10.733222799899522],
#     [4, 319.9650784003097, 635.5689940010052, 637.6496478002082],
#     [5, 6.849676198544332, 36.86405830230797, 35.08654409961309],
#     [6, 736.8222681998304, 736.1272995989566, 747.6204743998096],
#     [7, 762.3605406992283, 729.1856137017021, 783.2845127002656],
#     [8, 802.0422464000148, 800.3269172990258, 798.1906367989723]
# ]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the data points as dots
for test_no, value1, value2, value3 in data:
    ax.scatter(test_no, value1, color='r', marker='o', label='Run 1')
    ax.scatter(test_no, value2, color='g', marker='+', label='Run 2')
    ax.scatter(test_no, value3, color='b', marker='x', label='Run 3')

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
plt.title('Desc Sort Size Query', fontsize=16)

# Show the plot
plt.show()