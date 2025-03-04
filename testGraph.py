import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, CubicSpline

# Load dataset
df = pd.read_csv("data/QuantathonProvided.csv")  # Ensure your dataset has "Date" and "SP500" columns
df["Date"] = pd.to_datetime(df["Date"])  # Convert date to datetime
df["DateNum"] = (df["Date"] - df["Date"].min()).dt.days  # Convert dates to numerical format

# Extract x (dates as numbers) and y (S&P 500 values)
x = df["DateNum"].values
y = df["S&P500"].values

# Apply cubic spline interpolation
spline = CubicSpline(x, y)

# Generate smooth x values for interpolation
x_smooth = np.linspace(x.min(), x.max(), 500)  # 500 points for a smooth curve
y_smooth = spline(x_smooth)

# Plot original data and interpolated curve
plt.figure(figsize=(10, 5))
plt.plot(df["Date"], y, 'o', label="Original Data")  # Scatter plot for original points
plt.plot(pd.to_datetime(df["Date"].min()) + pd.to_timedelta(x_smooth, unit='D'), y_smooth, label="Interpolated Curve", linestyle='-')
plt.xlabel("Date")
plt.ylabel("S&P 500 Value")
plt.legend()
plt.title("S&P 500 Interpolated Curve")
plt.show()
