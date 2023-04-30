
# def plotTopPlayers(playerDF, n=30, rotation=75):
#     # Get the top n players with the highest placement percentile averages
#     top_n = playerDF.groupby('player')['avg_placement_percentile'].mean().nlargest(n).reset_index()
    
#     # Create a bar plot of the top n players with their percentile averages
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.bar(top_n['player'], top_n['avg_placement_percentile'])
#     ax.set_title(f'Top {n} Players by Placement Percentile Average')
#     ax.set_xlabel('Player Name')
#     ax.set_ylabel('Percentile Average')
#     ax.set_xticklabels(top_n['player'], rotation=rotation, fontsize=10)

#     # Add labels to the bar graph
#     labels = [f'{x:.2f}%' for x in top_n['avg_placement_percentile']]
#     ax.bar_label(ax.containers[0], labels=labels, label_type='edge')

#     plt.show()
from sheetsReadWriteFunctions import *

import matplotlib.pyplot as plt

# Dictionary with point values and names
docName = "2023 SJ Smash Sheet"
tourneySheetName = "2023 Q2 Tourneys"
clusterSheetName = '2023Q2 Player Clusters'
ptValueIncrement = 1.5
tier_list = getPlayerLevels(docName, clusterSheetName ,ptValueIncrement)

# Set up the figure and axis
fig, ax = plt.subplots()

# Plot the tier list
for point_value, names in tier_list.items():
    y_pos = [i for i in range(len(names))]
    ax.scatter([point_value] * len(names), y_pos, s=1000, alpha=0.5)
    for i, name in enumerate(names):
        ax.annotate(name, xy=(point_value, i), ha='center', va='center')

# Set the x-axis and y-axis labels
ax.set_xlabel('Point Value')
ax.set_ylabel('Player Names')

# Set the x-axis and y-axis limits
ax.set_xlim([0, max(tier_list.keys()) + 1])
ax.set_ylim([-1, max([len(names) for names in tier_list.values()])])

# Show the plot
plt.show()
