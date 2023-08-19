import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore', 'The iteration is not making good progress')

# Load the data from the Excel file
data = pd.read_excel('Assignment_Localization.xlsx')

# Extract the readings for each seat
readings_1D = data.iloc[4:14]
readings_1E = data.iloc[19:29]
readings_1F = data.iloc[35:45]

readings_1D.columns = data.iloc[3]
readings_1E.columns = data.iloc[3]
readings_1F.columns = data.iloc[3]

# Define the positions at which the reader antenna takes readings (0 cm, 8 cm, 16 cm, etc.)
positions = np.array([0, 8, 16, 24, 32, 40, 56, 64, 72, 80])  # in cm

# Find the median and mode for each seat
median_1D = np.median(readings_1D)
mode_1D = readings_1D.mode().iloc[0]
median_1E = np.median(readings_1E)
mode_1E = readings_1E.mode().iloc[0]
median_1F = np.median(readings_1F)
mode_1F = readings_1F.mode().iloc[0]

# Print the median and mode for each seat
print("Seat 1D: Median = {} Mode = {}\n".format(median_1D, mode_1D))
print("Seat 1E: Median = {} Mode = {}\n".format(median_1E, mode_1E))
print("Seat 1F: Median = {} Mode = {}\n".format(median_1F, mode_1F))

print(f" readings for each set {readings_1D.shape}, {readings_1E.shape}, {readings_1F.shape}\n")
# Convert phase readings from degrees to radians
readings_1D = np.radians(list(readings_1D['Position']))
# import pdb; pdb.set_trace()
readings_1E = np.radians(list(readings_1E['Position']))
readings_1F = np.radians(list(readings_1F['Position']))

print(f"The readings converted from 1D 1E 1F from degrees to radians are respectively:\n{readings_1D},\n{readings_1E}\n{readings_1F}\n")

# Calculate phase differences
phase_diffs_1D = np.diff(readings_1D)
phase_diffs_1E = np.diff(readings_1E)
phase_diffs_1F = np.diff(readings_1F)

print(f"phase difference for 1D: {phase_diffs_1D}\n phase difference for 1E {phase_diffs_1E}\n phase difference for 1F {phase_diffs_1F}\n")

# Calculate distance differences
lambda_ = 3e8 / 867e6  # wavelength for 815 MHz frequency
print(f" the wavelength is {lambda_}\n")
distance_diffs_1D = lambda_ * phase_diffs_1D / (4 * np.pi)
distance_diffs_1E = lambda_ * phase_diffs_1E / (4 * np.pi)
distance_diffs_1F = lambda_ * phase_diffs_1F / (4 * np.pi)

print(f" the distance difference for 1D:\n{distance_diffs_1D}\n for 1F:\n{distance_diffs_1F}\n for 1E: {distance_diffs_1E}\n")
# Calculate a, b, h for each seat
a_1D = distance_diffs_1D / 2
b_1D = np.sqrt(16 - a_1D ** 2)
# import pdb; pdb.set_trace()
h_1D = positions[:-1] + a_1D

print(f"The A B and H for 1D are respectively: {a_1D}{b_1D}{h_1D}\n")

a_1E = distance_diffs_1E / 2
b_1E = np.sqrt(16 - a_1E ** 2)
h_1E = positions[:-1] + a_1E

print(f"The A B and H for 1E are respectively: {a_1E}{b_1E}{h_1E}\n")

a_1F = distance_diffs_1F / 2
b_1F = np.sqrt(16 - a_1F ** 2)
h_1F = positions[:-1] + a_1F

print(f"The A B and H for 1F are respectively: {a_1F}{b_1F}{h_1F}\n")


# Define the hyperbola equations
def hyperbola(x, y, a, b, h):
    return (y - h) ** 2 / a ** 2 - x ** 2 / b ** 2 - 1


# Define the system of equations
def system_of_equations(vars, a_1D, b_1D, h_1D, a_1E, b_1E, h_1E, a_1F, b_1F, h_1F):
    x, y = vars
    eq1 = hyperbola(x, y, a_1D, b_1D, h_1D)
    eq2 = hyperbola(x, y, a_1E, b_1E, h_1E)
    eq3 = hyperbola(x, y, a_1F, b_1F, h_1F)
    return [eq1, eq2]


# Initialize lists to store the x and y coordinates of the intersection points
x_coords = []
y_coords = []

# Solve the system of equations for each set of a, b, h values
for i in range(len(positions) - 1):
    x, y = fsolve(system_of_equations, (0, 0),
                  args=(a_1D[i], b_1D[i], h_1D[i], a_1E[i], b_1E[i], h_1E[i], a_1F[i], b_1F[i], h_1F[i]))
    x_coords.append(x)
    y_coords.append(y)

# Calculate the centroid
centroid_x = sum(x_coords) / len(x_coords)
centroid_y = sum(y_coords) / len(y_coords)

print(f"The centroid of the intersection points is at ({centroid_x}, {centroid_y}).")


# Define a function to plot the hyperbola in quadratic form
def plot_hyperbola_quadratic(a, b, h):
    x = np.linspace(-20, 100, 500)  # Adjust the x range as needed
    y = a * (x - h) ** 2 + b
    return x, y


# Plot the hyperbolas for each seat
fig, ax = plt.subplots()
for i in range(len(positions) - 1):
    x, y = plot_hyperbola_quadratic(a_1D[i], b_1D[i], h_1D[i])
    ax.plot(x, y, label=f"Seat 1D-{i + 1}")

    x, y = plot_hyperbola_quadratic(a_1E[i], b_1E[i], h_1E[i])
    ax.plot(x, y, label=f"Seat 1E-{i + 1}")

    x, y = plot_hyperbola_quadratic(a_1F[i], b_1F[i], h_1F[i])
    ax.plot(x, y, label=f"Seat 1F-{i + 1}")

# Set axis labels and title
ax.set_xlabel('X Position (cm)')
ax.set_ylabel('Y Position (cm)')
ax.set_title('Hyperbolas for Each Seat (Quadratic Form)')

# Add a legend
ax.legend()

# Show the plot
plt.grid()
plt.show()