from manim import *
import pandas as pd
import numpy as np
import math

class histogram(Scene):
    def construct(self):
        buckets = 10
        df = pd.read_csv("data/Salary_Data.csv")
        df['Age_Bin'], bin_edges = pd.cut(df['Age'], bins=buckets, retbins=True, labels=False)

        hist_counts = df['Age_Bin'].value_counts(sort=False).to_numpy()

        ax = Axes(
            x_range=[0,buckets], 
            y_range=[0,math.ceil(hist_counts.max() / 100) * 100, int((math.ceil(hist_counts.max() / 100) * 100)/10)], 
            tips=False, 
            axis_config={"include_numbers": False}, 
            y_axis_config={"include_numbers": True}
        )
        
        labels = VGroup()
        for i, edge in enumerate(bin_edges):
            label = MathTex(f"{edge:.0f}").scale(.75)  # Format with 1 decimal place
            label.next_to(ax.c2p(i, 0), DOWN, buff=0.2)  # Place below x-axis
            labels.add(label)
        
        self.play(Create(ax), Write(labels))
        self.wait()
        
        x_tick_width = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        y_tick_height = ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]
        
        rects = VGroup()
        
        for i in range(buckets):
            rect = Rectangle(height=y_tick_height*hist_counts[i], width=x_tick_width, color=BLUE, fill_opacity=.4)
            rect.move_to(ax.c2p(i,0), aligned_edge=DL)
            rects.add(rect)
        
        rects.set_color_by_gradient(BLUE,GREEN,YELLOW)
        
        # self.play(DrawBorderThenFill(vg))
        self.play(LaggedStart(*[DrawBorderThenFill(rect) for rect in rects], lag_ratio=0.05))
        self.wait()
        
        histoGroup = VGroup(labels, ax, rects)
        
        self.play(histoGroup.animate.scale(.5))
        self.play(histoGroup.animate.shift(UP*2, LEFT*3))
        
        self.wait(3)
        
        
        
        
        