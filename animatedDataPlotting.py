from manim import *
import pandas as pd
import numpy as np
import math
from scipy.interpolate import CubicSpline

class Intro(Scene):
    def construct(self):
        t = Text("Hello").shift(UP)
        self.play(Write(t))
        self.wait(2)
        self.play(FadeOut(t))
        self.wait(1)

class PlotExample(Scene):
    def construct(self):
        
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1, 5, 1], tips=False)
        vt = ValueTracker(-5)

        f1_func = lambda x: (1 / 5) * x**2
        f2_func = lambda x: 2*math.sin(x)+1

        # Define the curves
        f1 = always_redraw(lambda: ax.plot(f1_func, color=BLUE, x_range=[-5, vt.get_value()]))
        f2 = always_redraw(lambda: ax.plot(f2_func, color=YELLOW, x_range=[-5, vt.get_value()]))

        # Function to generate the shading area dynamically
        def get_shaded_region():
            x_values = np.linspace(-5, vt.get_value(), 50)  # Generate x values
            points = [ax.c2p(x, f1_func(x)) for x in x_values]  # Upper curve points
            points += [ax.c2p(x, f2_func(x)) for x in reversed(x_values)]  # Lower curve points (reversed)
            return Polygon(*points, color=GREEN, fill_opacity=0.5, stroke_width=0)  # Create the shaded area

        # Always redraw the shaded area
        shaded_region = always_redraw(get_shaded_region)

        # Moving dots on each curve
        f1_dot = always_redraw(lambda: Dot(point=ax.c2p(vt.get_value(), f1_func(vt.get_value())), color=BLUE))
        f2_dot = always_redraw(lambda: Dot(point=ax.c2p(vt.get_value(), f2_func(vt.get_value())), color=YELLOW))
        
        x_label = always_redraw(lambda: MathTex(f"x={vt.get_value():.1f}")  # Format to 2 decimal places
            .to_corner(UR)  # Position in the Upper Right
            .scale(0.8)  # Adjust size
        )

        self.play(Write(ax))
        self.wait()

        # Add everything including the dynamically updating shaded region
        self.add(f1, f2, shaded_region, f1_dot, f2_dot, x_label)
        self.play(vt.animate.set_value(5), run_time=6)

        self.play(FadeOut(f1_dot), FadeOut(f2_dot))
        self.wait()
        
class ScatterInterpolate(Scene):
    def construct(self):
        # Load dataset
        df = pd.read_csv("data/QuantathonProvided.csv")  # Ensure columns: "Date", "SP500"
        df["Date"] = pd.to_datetime(df["Date"])
        df["DateNum"] = (df["Date"] - df["Date"].min()).dt.days  # Convert to numerical x-axis

        x = df["DateNum"].values
        y = df["S&P500"].values

        # Apply cubic spline interpolation
        spline = CubicSpline(x, y)
        x_smooth = np.linspace(x.min(), x.max(), 100)  # 100 smooth points
        y_smooth = spline(x_smooth)

        # Define graph axes
        axes = Axes(
            x_range=[x.min(), x.max(), 365],  # Adjust ticks for clarity
            y_range=[min(y)-100, max(y)+100, (max(y)-min(y))/5],  # Adjust for better scaling
            axis_config={"color": WHITE, "include_numbers": True},
        ).scale(0.9)
        
        labels = axes.get_axis_labels(
            Tex("Year").scale(0.7), Text("S&P 500 Price").scale(0.45)
        )

        # Convert data points to Manim-friendly format
        def graph_func(x_val):
            return spline(x_val)  # Manim will call this function to plot

        # Create graph from function
        graph = axes.plot(graph_func, color=BLUE)

        # Add labels
        title = Text("S&P 500 Interpolated Curve").scale(0.8).to_edge(UP)

        # Animate scene
        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=3)
        self.wait(2)



class DoubleScatter(Scene):
    def construct(self):
        # Load dataset
        pred_df = pd.read_csv("data/predictions_2019_2022.csv")

        # Convert dates to datetime
        pred_df["Date"] = pd.to_datetime(pred_df["Date"])

        # Filter date range: 2019-01-02 to 2022-12-31
        start_date = "2019-01-02"
        end_date = "2022-12-31"
        pred_df = pred_df[(pred_df["Date"] >= start_date) & (pred_df["Date"] <= end_date)]

        # Convert dates to numerical format
        pred_df["DateNum"] = (pred_df["Date"] - pred_df["Date"].min()).dt.days

        # Extract values
        x_pred = pred_df["DateNum"].values
        y_pred = pred_df["Portfolio Value"].values

        x_sp500 = pred_df["DateNum"].values
        y_sp500 = pred_df["Buy & Hold Value"].values

        # Apply cubic spline interpolation
        spline_pred, spline_sp500 = CubicSpline(x_pred, y_pred), CubicSpline(x_sp500, y_sp500)

        # Generate smooth x values
        x_smooth = np.linspace(min(x_pred.min(), x_sp500.min()), max(x_pred.max(), x_sp500.max()), 150)

        # Define graph axes
        axes = Axes(
            x_range=[x_smooth.min(), x_smooth.max(), (x_smooth.max() - x_smooth.min()) / 10],
            y_range=[min(y_pred.min(), y_sp500.min()), max(y_pred.max(), y_sp500.max()), (max(y_pred.max(), y_sp500.max()) - min(y_pred.min(), y_sp500.min())) / 5],
            axis_config={"color": WHITE}
        ).scale(0.9)

        # Define graph functions
        def portfolio_func(x_val): return spline_pred(x_val)
        def sp500_func(x_val): return spline_sp500(x_val)

        # Create graphs
        portfolio_graph = axes.plot(portfolio_func, color=ORANGE)
        sp500_graph = axes.plot(sp500_func, color=BLUE)

        # Create ValueTrackers for animation
        tracker = ValueTracker(x_smooth[0])

        # Moving dots at the end of each graph
        portfolio_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), portfolio_func(tracker.get_value())), color=ORANGE))
        sp500_dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), sp500_func(tracker.get_value())), color=BLUE))

        # Labels above the dots
        portfolio_label = always_redraw(lambda: Text(f"Portfolio: {portfolio_func(tracker.get_value()):.0f}", color=ORANGE, font_size=24).next_to(portfolio_dot, UP))
        sp500_label = always_redraw(lambda: Text(f"S&P 500: {sp500_func(tracker.get_value()):.0f}", color=BLUE, font_size=24).next_to(sp500_dot, DOWN))
        
        portfolio_label.set_z_index(999)
        sp500_label.set_z_index(999)

        # Add title and legend
        title = Text("Portfolio Value vs. S&P 500 (2019-2022)").scale(0.8).to_edge(UP)
        legend = VGroup(
            Dot(color=ORANGE), Text("Portfolio Value").scale(0.6),
            Dot(color=BLUE), Text("S&P 500").scale(0.6)
        ).arrange(RIGHT).to_edge(DOWN)

        # Animate
        self.play(Write(title))
        self.play(Create(axes))
        self.add(portfolio_dot, sp500_dot, portfolio_label, sp500_label)
        self.play(Create(portfolio_graph), Create(sp500_graph), tracker.animate.set_value(x_smooth[-1]), run_time=10, rate_func=smooth)
        self.play(FadeIn(legend, shift=UP))

        self.wait(2)
    