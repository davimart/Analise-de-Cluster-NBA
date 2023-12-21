import matplotlib.pyplot as plt

# Sample data
x_values = [1, 2, 3, 4, 5]
y_values = [2, 4, 6, 8, 10]

# Plot the graph
plt.plot(x_values, y_values, label='Example Graph')

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Graph Example')

# Display the list of values on the right side of the graph as subtitles
for x, y in zip(x_values, y_values):
    plt.text(max(x_values) + 0.1, y, f'({x}, {y})', ha='left', va='center', color='red')

# Show the plot
plt.show()

