from manim import *
import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LinearRegression

class scene(Scene):
    def construct(self):
        demo.construct(self)
        MultiGraph.construct(self)
        
class Intro(Scene):
    def construct(self):
        # Colors
        colors = [RED, GREY, WHITE]#, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK]
        
        # Create random geometric shapes
        shapes = VGroup()
        
        positions = [
            [-4, 2, 0], [-2, 2.75, 0], [0, 1.5, 0], [2, 2.5, 0], [5, 2, 0],
            [-5, 0, 0], [-2.5, -0.5, 0], [0, -1, 0], [2.5, 1.5, 0], [4.5, 0, 0],
            [-4.5, -2, 0], [-2, -1.5, 0], [0, -2, 0], [2, -3, 0], [4, -2, 0]
        ]
        
        for pos in positions:
            shape_type = random.choice([Square, Circle, Triangle])
            shape = shape_type()
            shape.set_fill(random.choice(colors), opacity=0.8)
            shape.set_stroke(WHITE, width=2)
            shape.scale(random.uniform(0.75, 1.5))
            shape.move_to(pos)
            shape.rotate(random.uniform(0, 360) * DEGREES)
            shapes.add(shape)
        
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in shapes], lag_ratio=0.1), run_time=2)
        self.wait(1)
        
        # Animate shapes into letters
        letters = Text("NORTON ANTIVIRUS", font_size=72, color=WHITE)
        
        # Load the SVG image
        ohio_logo = SVGMobject("Ohio_State_Buckeyes_logo1.svg")  # Make sure the path is correct
        ohio_logo.scale(3)  # Adjust size as needed
        
        # Animate the SVG logo into the letters
        letters = Text("NORTON ANTIVIRUS", font_size=72, color=WHITE)
        self.play(Transform(shapes, letters), run_time=3)
        self.wait(3)
        
        
        # Animate the transformation from shapes to the SVG
        self.play(Transform(shapes, ohio_logo), run_time=3)
        self.wait(2)

        self.play(FadeOut(shapes), run_time=1)

class demo(Scene):
    def construct(self):
        t = Text("Hello!").shift(UP)
        t2 = Tex("Hi!").shift(DOWN)
        self.play(Write(t), Write(t2))
        self.wait(3)
        self.play(FadeOut(t), FadeOut(t2))
        self.wait(1)

class Test(Scene):
    def construct(self):
        # Load dataset (only first 100 rows)
        df = pd.read_csv("datasets/japan_heart_attack_dataset.csv").head(500)

        # Extract Age and Cholesterol_Level columns
        ages = df["Age"].to_numpy()
        cholesterol_levels = df["Stress_Levels"].to_numpy()

        # Create a scatter plot using Manim
        scatter = Axes(
            x_range=[0, max(ages) + 5, 10],  # Extend range slightly for spacing
            y_range=[0, max(cholesterol_levels) + 10, 5],
            # axis_config={"include_tip": False, "numbers_to_include": range(20, 100, 20)},
            axis_config={"include_tip": False},
            x_length=7,
            y_length=5,
        ).add_coordinates()

        # Labels
        x_label = scatter.get_x_axis_label("Age")
        y_label = scatter.get_y_axis_label("Stress Levels")

        # Convert (Age, Cholesterol_Level) to Manim coordinates and plot dots
        scatter_dots = VGroup(*[
            Dot(scatter.c2p(age, chol), color=RED, radius=0.05) for age, chol in zip(ages, cholesterol_levels)
        ])

        # Add elements to scene
        self.play(Create(scatter), FadeIn(x_label, y_label))
        self.play(LaggedStartMap(FadeIn, scatter_dots, lag_ratio=0.1))
        self.wait(2)
        
        # a = [-2, 0, 0]
        # b = [2, 0, 0]
        # c = [0, 2*np.sqrt(3), 0]
        # p = [0.37, 1.4, 0]
        # dota = Dot(a, radius=0.06,color=WHITE)
        # dotb = Dot(b, radius=0.06,color=WHITE)
        # dotc = Dot(c, radius=0.06,color=WHITE)
        # dotp = Dot(p, radius=0.06,color=WHITE)
        # lineap = Line(dota.get_center(), dotp.get_center()).set_color(WHITE)
        # linebp = Line(dotb.get_center(), dotp.get_center()).set_color(WHITE)
        # linecp = Line(dotc.get_center(), dotp.get_center()).set_color(WHITE)
        # equilateral = Polygon(a,b,c)
        # triangle = Polygon(a,b,p)
        # self.play(Write(equilateral))
        # self.wait()
        # self.play(Write(VGroup(lineap,linebp,linecp,triangle)))
        # self.wait()
        # self.play(triangle.animate.rotate(0.4))
        # self.wait()
        
class MultiGraph(Scene):
    def construct(self):
        # Load dataset (first 100 rows)
        df = pd.read_csv("datasets/japan_heart_attack_dataset.csv").head(100)

        # Extract relevant columns
        ages = df["Age"].to_numpy()
        stress_levels = df["Stress_Levels"].to_numpy()
        cholesterol_levels = df["Cholesterol_Level"].to_numpy()
        bmi = df["BMI"].to_numpy()
        heart_rate = df["Heart_Rate"].to_numpy()

        # Function to compute line of best fit
        def best_fit_line(x_data, y_data, scatter):
            m, b = np.polyfit(x_data, y_data, 1)  # Linear regression
            x_min, x_max = min(x_data), max(x_data)
            line = Line(
                scatter.c2p(x_min, m * x_min + b), 
                scatter.c2p(x_max, m * x_max + b),
                color=BLUE, stroke_width=3
            )
            return line

        # Function to create a compressed scatter plot
        def create_scatter_plot(x_data, y_data, title_text, scale_factor=0.7, shift_vector=ORIGIN):
            scatter = Axes(
                x_range=[min(x_data) - 5, max(x_data) + 5, 10],
                y_range=[min(y_data) - 5, max(y_data) + 5, 10],
                axis_config={"include_tip": False, "font_size": 20},
                x_length=5.5,  
                y_length=4.5 * 0.9,  # Compress y-axis height by 90%
            ).add_coordinates()

            # Reduce number font size for clarity
            for num in scatter.get_x_axis().numbers + scatter.get_y_axis().numbers:
                num.set_font_size(14)

            # Scatter dots (initially invisible)
            scatter_dots = VGroup(*[
                Dot(scatter.c2p(x, y), color=RED, radius=0.05).set_opacity(0) for x, y in zip(x_data, y_data)
            ])

            # Title above the graph
            title = Text(title_text, font_size=28).next_to(scatter, UP)

            # Best fit line (initially hidden)
            best_fit = best_fit_line(x_data, y_data, scatter).set_opacity(0)

            # Group and position
            plot_group = VGroup(scatter, title, scatter_dots, best_fit)
            plot_group.scale(scale_factor).shift(shift_vector)
            return plot_group, scatter_dots, best_fit

        # Create all 4 scatter plots with compressed height
        top_left, dots_tl, line_tl = create_scatter_plot(ages, stress_levels, "Age vs Stress Levels", shift_vector=UP * 2 + LEFT * 3)
        top_right, dots_tr, line_tr = create_scatter_plot(ages, cholesterol_levels, "Age vs Cholesterol", shift_vector=UP * 2 + RIGHT * 3)
        bottom_left, dots_bl, line_bl = create_scatter_plot(ages, bmi, "Age vs BMI", shift_vector=DOWN * 2 + LEFT * 3)
        bottom_right, dots_br, line_br = create_scatter_plot(ages, heart_rate, "Age vs Heart Rate", shift_vector=DOWN * 2 + RIGHT * 3)

        # Display all graphs
        self.play(
            FadeIn(top_left),
            FadeIn(top_right),
            FadeIn(bottom_left),
            FadeIn(bottom_right),
        )

        # Staggered point animation for all charts
        def animate_dots(dots):
            return AnimationGroup(*[dot.animate.set_opacity(1) for dot in dots], lag_ratio=0.05)

        self.play(
            animate_dots(dots_tl),
            animate_dots(dots_tr),
            animate_dots(dots_bl),
            animate_dots(dots_br),
        )
        self.wait(1)

        # Show lines of best fit after points render
        self.play(
            line_tl.animate.set_opacity(1),
            line_tr.animate.set_opacity(1),
            line_bl.animate.set_opacity(1),
            line_br.animate.set_opacity(1),
        )
        self.wait(2)

        # Zoom into "Age vs. Stress Levels"
        self.play(
            top_left.animate.scale(2).move_to(ORIGIN),
            FadeOut(top_right),
            FadeOut(bottom_left),
            FadeOut(bottom_right),
        )
        self.wait(2)
        
        top_right.move_to(ORIGIN).scale(2).set_opacity(0)
        self.play(Transform(top_left, top_right.set_opacity(1), path_arc=PI/2))
        self.wait(3)
        
        # self.play(
        #     bottom_right.animate.scale(2).move_to(ORIGIN),
        #     top_right.animate.scale(2).move_to(LEFT),
        #     FadeOut(top_right),
        # )
        # self.wait(3)
        
        # self.play(
        #     bottom_left.animate.scale(2).move_to(ORIGIN),
        #     bottom_right.animate.scale(2).move_to(LEFT),
        #     FadeOut(bottom_right),
        # )
        # self.wait(3)
        
class ThreeDScatter(ThreeDScene):
    def construct(self):
        # Load dataset (first 50 rows)
        # df = pd.read_csv("datasets/japan_heart_attack_dataset.csv").head(100)
        df = pd.read_csv("hackathon/data/CO2 Emissions_Canada.csv").head(100)

        # Extract relevant columns
        # ages = df["Age"].to_numpy()
        # stress_levels = df["Stress_Levels"].to_numpy()
        # cholesterol_levels = df["Cholesterol_Level"].to_numpy()
        
        ages = df["Cylinders"].to_numpy()
        stress_levels = df["Fuel Consumption City (L/100 km)"].to_numpy()
        cholesterol_levels = df["Fuel Consumption Hwy (L/100 km)"].to_numpy()

        # Create 3D Axes
        axes = ThreeDAxes(
            # x_range=[18, 80, 10],  # Age
            # y_range=[0, 10, 2],    # Stress Levels
            # z_range=[100, 250, 50],  # Cholesterol Level
            x_range=[2, 14, 2],  # Cyl
            y_range=[2, 20, 2],    # City
            z_range=[2, 20, 2],  # Hwy
            x_length=5,
            y_length=5,
            z_length=5,
        )
        
        axes.move_to(DOWN * .3)
        self.camera.set_zoom(.8)  # Increase the zoom-out level

        # Axis labels
        x_label = Text("Cylinders").next_to(axes.x_axis, RIGHT)
        y_label = Text("Fuel Consumption City").next_to(axes.y_axis, UP)
        z_label = Text("Fuel Consumption Hwy").next_to(axes.z_axis, OUT)
        
        x_label.rotate(90 * DEGREES, axis=RIGHT)
        y_label.rotate(90 * DEGREES, axis=RIGHT)
        z_label.rotate(90 * DEGREES, axis=RIGHT)
        
        def update_label_rotation(label):
            label.rotate(-0.2 * DEGREES, axis=OUT)

        # Apply the updater so the labels rotate at the same rate as the camera
        x_label.add_updater(lambda m, dt: m.rotate(0.2 * dt, axis=OUT))
        y_label.add_updater(lambda m, dt: m.rotate(0.2 * dt, axis=OUT))
        z_label.add_updater(lambda m, dt: m.rotate(0.2 * dt, axis=OUT))

        labels = VGroup(x_label, y_label, z_label)

        # Create scatter points
        points = VGroup()
        for age, stress, cholesterol in zip(ages, stress_levels, cholesterol_levels):
            point = Dot3D(point=axes.c2p(age, stress, cholesterol), radius=0.06, color=GREY)
            points.add(point)

        # Set initial opacity for staggered effect
        for p in points:
            p.set_opacity(0)


        # Prepare data for regression (reshaped for sklearn)
        X = np.column_stack((ages, stress_levels))  # Independent variables (Age, Stress)
        y = cholesterol_levels  # Dependent variable (Cholesterol)

        # Fit a linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Get regression coefficients
        a, b = model.coef_
        c = model.intercept_

        # # Define the 3D line of best fit as a parametric function
        # best_fit_line = ParametricFunction(
        #     lambda t: axes.c2p(
        #         18 + t * (80 - 18),  # Age range
        #         0 + t * (10 - 0),    # Stress range
        #         c + a * (18 + t * (80 - 18)) + b * (0 + t * (10 - 0))  # Predicted Cholesterol
        #     ),
        #     t_range=[0, 1],
        #     color=RED
        # )
        
        # Define the 3D line of best fit as a parametric function
        best_fit_line = ParametricFunction(
            lambda t: axes.c2p(
                2 + t * (14 - 2),  # Cyl range
                2 + t * (20 - 2),  # City range
                c + a * (2 + t * (14 - 2)) + b * (2 + t * (20 - 2))  # Predicted Hwy
            ),
            t_range=[0, 1],
            color=RED
        )

        

        # Set camera orientation
        self.set_camera_orientation(phi=70 * DEGREES, theta=-90 * DEGREES)

        # Add axes and labels
        self.add(axes, labels)
        
        # Enable ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        # Animate points with staggered lag effect
        self.play(
            LaggedStart(*[p.animate.set_opacity(1) for p in points], lag_ratio=0.1),
            run_time=3
        )
        
        # Animate the best-fit line after the points
        self.play(Create(best_fit_line), run_time=2)
        
        self.wait(3)
        
        
class AiExplained(Scene):
    def construct(self):
        # Load dataset and sample 50 rows for each plot
        df = pd.read_csv("hackathon/data/CO2 Emissions_Canada.csv")
        
        # Define columns to plot against CO2 Emissions
        columns = ["Vehicle Class", "Engine Size(L)", "Cylinders", "Transmission", "Fuel Type"]
        y_positions = np.linspace(3, -3, 5)  # Spread vertically
        left_x = -4  # Left side positioning
        
        # Load and display robot.svg in center
        robot = SVGMobject("robot.svg").scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(robot))

        scatter_plots = VGroup()
        scatter_dots = VGroup()
        
        # Create labeled scatter plots
        for i, col in enumerate(columns):
            sampled_data = df.sample(20)  # Random 50 samples
            
            # Create axes for scatter plot
            axes = Axes(
                x_range=[0, 10, 5],  # Adjust for categorical scaling
                y_range=[df["CO2 Emissions(g/km)"].min(), df["CO2 Emissions(g/km)"].max(), 150],
                x_length=1.5,
                y_length=1.5,
                axis_config={"color": WHITE}
            ).move_to([left_x, y_positions[i], 0])
            
            axes.x_axis.remove(axes.x_axis.tip)  # Remove the x-axis arrow
            axes.y_axis.remove(axes.y_axis.tip)

            # Add labels
            x_label = Text("", font_size=18).next_to(axes.x_axis, RIGHT)
            y_label = Text(col, font_size=18).next_to(axes.y_axis, LEFT)

            dots = VGroup()
            for _, row in sampled_data.iterrows():
                # Normalize X values for categorical data
                if df[col].dtype == object:  # Categorical data
                    x_value = hash(row[col]) % 10  # Random mapping for categories
                else:
                    x_value = row[col]
                
                # Create a dot
                dot = Dot(color=RED).move_to(axes.c2p(x_value, row["CO2 Emissions(g/km)"]))
                dots.add(dot)


            scatter_dots.add(dots)
            scatter_plots.add(axes, x_label, y_label, dots)

        # Add scatter plots to the scene
        self.play(LaggedStart(*[FadeIn(plots) for plots in scatter_plots], lag_ratio=0.2), run_time=2)
        self.wait(1)

        # Move all dots to robot.svg location (assumed at origin)
        self.play(*[d.animate.move_to(ORIGIN) for d in scatter_dots], run_time=2)

        # Fade out all dots
        self.play(FadeOut(scatter_dots), run_time=1)
        self.wait(0.5)

        # Persistent labels for MPG and CO2 values
        mpg_text = Text("Miles Per Gallon:", font_size=30).move_to([3.75, 1, 0])
        co2_text = Text("CO2 Emissions(g/km):", font_size=30).move_to([3.75, -1, 0])
        self.play(Write(mpg_text), Write(co2_text))

        # Create initial MPG and CO2 value text objects
        mpg_value = Text("", font_size=30).next_to(mpg_text, RIGHT)
        co2_value = Text("", font_size=30).next_to(co2_text, RIGHT)
        mpg_value.move_to([3, 1, 0])
        co2_value.move_to([3, 1, 0])
        self.play(FadeIn(mpg_value), FadeIn(co2_value))

        # Reintroduce dots moving to display MPG and CO2
        for _ in range(5):
            mpg = random.randint(20, 40)
            co2 = random.randint(100, 300)

            # Generate 2 dots
            dot1 = Dot(color=RED).move_to(robot.get_center())
            dot2 = Dot(color=RED).move_to(robot.get_center())
            

            # Create new text objects for the updated values
            new_mpg_value = Text(str(mpg), font_size=30).next_to(mpg_text, RIGHT)
            new_co2_value = Text(str(co2), font_size=30).next_to(co2_text, RIGHT)

            # Move dots and update values
            self.play(
                FadeOut(dot1, dot2),
                dot1.animate.move_to([5.25, 1, 0]),
                dot2.animate.move_to([5.25, -1, 0]),
                ReplacementTransform(mpg_value, new_mpg_value),
                ReplacementTransform(co2_value, new_co2_value),
                run_time=1.5
            )

            # Update the references to the current text objects
            mpg_value = new_mpg_value
            co2_value = new_co2_value

            # Remove dots but keep labels
            self.play(FadeOut(dot1, dot2), run_time=1)

        self.wait(2)
        
        
class Team(Scene):
    def construct(self):
        # Define the text to display
        team_members = [
            "Arjun Anand: Freshman CSE Major, Predictive Model Lead",
            "Caden Conde: Freshman CIS Major, Visualization & Insight Lead",
            "Ryan Lee: Freshman Logistics Major, Statistics & External Research Lead",
            "Auritro Saha: Freshman CSE Major, Data Cleaning & Presentation Lead"
        ]

        # Create the initial text object
        text = Text(team_members[0], font_size=30, color=RED)
        self.play(Write(text), run_time=2)
        self.wait(5)

        # Replace the text for each team member
        for member in team_members[1:]:
            new_text = Text(member, font_size=30, color=RED)
            self.play(ReplacementTransform(text, new_text), run_time=2)
            text = new_text  # Update the reference to the current text
            self.wait(5)

        # Fade out everything at the end
        self.play(FadeOut(text), run_time=2)


class Tools(Scene):
    def construct(self):
        # Title: "Tools Used" in large red text
        title = Text("Tools Used", font_size=60, color=RED).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Define the categories and tools
        categories = {
            "Collab/Version Control": ["VSCode", "Git"],
            "Statistical Analysis": ["Numpy", "Pandas"],
            "Plotting/Visualization": ["PlotLy", "MatPlotLib", "Manim (Presentation)", "Folium (Maps)"],
            "AI/ML Predictive Model": ["SciKitLearn"],
            "Front End": ["React"]
        }

        # Display each category and its tools at the origin
        for category, tools in categories.items():
            # Create the category text
            category_text = Text(category, font_size=40, color=WHITE).move_to(UP)
            self.play(Write(category_text), run_time=1)
            self.wait(0.5)

            # Create the tools as bullet points
            tool_texts = VGroup()  # Group to hold all tool texts
            for tool in tools:
                tool_text = Text(f"• {tool}", font_size=30, color=GREY)
                tool_texts.add(tool_text)

            # Arrange tools vertically below the category
            tool_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(category_text, DOWN, buff=0.5)

            # Write the tools one by one
            for tool_text in tool_texts:
                self.play(FadeIn(tool_text, shift=RIGHT), run_time=0.5)

            # Wait for a moment before fading out
            self.wait(1)

            # Fade out the category and tools
            self.play(FadeOut(category_text), FadeOut(tool_texts), run_time=1)

        # Fade out the title at the end
        self.play(FadeOut(title), run_time=1)
        
        
class ModelAccuracy(Scene):
    def construct(self):
        # Title: "Random Force Regression Model Prediction Accuracy" in red
        title = Text("Random Force Regression Model Prediction Accuracy", font_size=40, color=RED)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Subtitle: Split into two lines and centered
        subtitle_line1 = Text("Given Vehicle Class, Transmission Type, # of Cylinders,", font_size=24, color=WHITE)
        subtitle_line2 = Text("Engine Size, and Fuel Type, our model can predict:", font_size=24, color=WHITE)
        subtitle_group = VGroup(subtitle_line1, subtitle_line2).arrange(DOWN, buff=0.2)
        subtitle_group.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_line1, shift=UP), FadeIn(subtitle_line2, shift=UP), run_time=1.5)
        self.wait(1)

        # Bullet points
        bullet1 = Text("• CO2 Emission with an accuracy of ", font_size=24, color=WHITE)
        bullet2 = Text("• MPG with an accuracy of ", font_size=24, color=WHITE)

        # Animated numbers
        co2_accuracy = Text("95.9%", font_size=24, color=YELLOW)
        co2_rqse = Text("15.195", font_size=24, color=YELLOW)
        mpg_accuracy = Text("95.92%", font_size=24, color=YELLOW)
        mpg_rsme = Text("2.16", font_size=24, color=YELLOW)

        # Arrange bullet points and numbers
        bullet_group = VGroup(bullet1, bullet2).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        bullet_group.shift(LEFT*2)  # Move bullet points slightly to the left

        co2_accuracy.next_to(bullet1, RIGHT, buff=0.1)
        co2_rqse_text = Text("and a RQSE of ", font_size=24, color=WHITE).next_to(co2_accuracy, RIGHT, buff=0.1)
        co2_rqse.next_to(co2_rqse_text, RIGHT, buff=0.1)

        mpg_accuracy.next_to(bullet2, RIGHT, buff=0.1)
        mpg_rsme_text = Text("and a RSME of ", font_size=24, color=WHITE).next_to(mpg_accuracy, RIGHT, buff=0.1)
        mpg_rsme.next_to(mpg_rsme_text, RIGHT, buff=0.1)

        # Write bullet points
        self.play(FadeIn(bullet1, shift=RIGHT), FadeIn(bullet2, shift=RIGHT), run_time=1.5)
        self.wait(0.5)

        # Animate numbers for CO2 Emission
        self.play(
            FadeIn(co2_accuracy, shift=UP),
            FadeIn(co2_rqse_text, shift=UP),
            FadeIn(co2_rqse, shift=UP),
            run_time=1.5
        )
        self.play(
            co2_accuracy.animate.set_color(RED).scale(1.2),
            co2_rqse.animate.set_color(RED).scale(1.2),
            run_time=1
        )
        self.play(
            co2_accuracy.animate.set_color(YELLOW).scale(1 / 1.2),
            co2_rqse.animate.set_color(YELLOW).scale(1 / 1.2),
            run_time=1
        )
        self.wait(1)

        # Animate numbers for MPG
        self.play(
            FadeIn(mpg_accuracy, shift=UP),
            FadeIn(mpg_rsme_text, shift=UP),
            FadeIn(mpg_rsme, shift=UP),
            run_time=1.5
        )
        self.play(
            mpg_accuracy.animate.set_color(RED).scale(1.2),
            mpg_rsme.animate.set_color(RED).scale(1.2),
            run_time=1
        )
        self.play(
            mpg_accuracy.animate.set_color(YELLOW).scale(1 / 1.2),
            mpg_rsme.animate.set_color(YELLOW).scale(1 / 1.2),
            run_time=1
        )
        self.wait(1)

        # Fade out everything at the end
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)