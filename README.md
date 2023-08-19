# RFID Localization using Hyperbolic Triangulation

This repository contains Python code that demonstrates RFID localization using hyperbolic triangulation. The code processes RFID phase readings from multiple antennas to estimate the positions of RFID tags in a confined space. This technique is particularly useful for scenarios where traditional localization methods like GPS are not viable.

## Prerequisites

Before running the code, make sure you have the following:

- Python 3.10
- Required packages: `numpy`, `scipy`, `pandas`, and `matplotlib`

You can install these packages using the following command:

```bash
pip install numpy scipy pandas matplotlib
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/AbhiramInguva/rfid-localization.git
```

2. Navigate to the repository directory:

```bash
cd rfid-localization
```

3. Place your RFID data Excel file named `Assignment_Localization.xlsx` in the same directory as the code.

4. Run the Python script:

```bash
python rfid_localization.py
```

## Description

The provided code performs the following steps:

1. Loads RFID data from the Excel file using the `pandas` library.
2. Extracts the RFID readings for each seat and converts them from degrees to radians.
3. Calculates phase differences and distance differences using the RFID readings.
4. Estimates `a`, `b`, and `h` parameters for each seat using the calculated distance differences.
5. Defines hyperbola equations and a system of equations for intersection points.
6. Solves the system of equations to find the intersection points for each seat.
7. Calculates the centroid of the intersection points to estimate the RFID tag position.
8. Plots hyperbolas for each seat using the `matplotlib` library.

## Results

The centroid of the intersection points represents the estimated position of the RFID tag within the confined space. Hyperbolas for each seat are plotted to visualize the localization process.


Feel free to modify and improve the code according to your needs. If you encounter any issues or have questions, please open an issue in the repository. Happy coding!
