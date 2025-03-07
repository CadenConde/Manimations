from manim import *
import pandas as pd
import numpy as np
import math

class SharpeRatio(Scene):
    def construct(self):
        SRatio = MathTex(r"S = \left( \frac{R_p - R_f}{\sigma_p} \right)")
        SRatio_Copy = SRatio.copy()
                  
        top = Tex("54 - 4351")
        top[0][0:2].set_color(BLUE)
        top[0][3:9].set_color(YELLOW)    
            
        top2 = Tex("4405").set_color(GREEN)
                  
        self.wait()
        self.play(Write(SRatio))
        self.add(SRatio_Copy)
        self.wait()
        
        SRatio_Copy[0][3:5].set_color(BLUE)
        SRatio_Copy[0][6:8].set_color(YELLOW)

        self.play(
            SRatio.animate.shift(LEFT * 3), 
            SRatio_Copy.animate.set_opacity(1).shift(RIGHT * 3), 
        )

        # Transform only the isolated substrings
        self.play(
            Transform(SRatio_Copy[0][3:8], top.move_to(SRatio_Copy[0][3:8])),
        )

        self.wait()
        
        self.play(
            Transform(SRatio_Copy[0][3:8], top2.move_to(SRatio_Copy[0][3:8])),
        )

        self.wait(2)