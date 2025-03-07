from manim import *
import math

class Waves2d(Scene):
    def construct(self):
        vt = ValueTracker(0)
        formula = MathTex(r"X(f) = \int_{-\infty}^{\infty}x(t)e^{-j2\pi ft}dt").scale(1)
        
        Ax = Axes(x_range=[-30,30], y_range=[-8,8])
        Wave1 = Ax.plot(lambda x: math.sin((x-2*vt.get_value()))+math.cos((x-vt.get_value())*1.2)+math.sin((x-0.5*vt.get_value())*.7), color=WHITE)
        
        subWave0 = Ax.plot(lambda x: math.sin((x-2*vt.get_value())))
        subWave1 = Ax.plot(lambda x: math.cos((x-vt.get_value())*1.2))
        subWave2 = Ax.plot(lambda x: math.sin((x-0.5*vt.get_value())*.7))
        
        subWaves = VGroup(subWave0, subWave1, subWave2)
        subWaves.set_color_by_gradient(RED,YELLOW)
        
        self.play(Create(Wave1))
        self.wait(1)
        self.play(
            ReplacementTransform(Wave1, subWaves),
        )
        self.play(
            AnimationGroup(
                subWaves[2].animate.next_to(subWaves[1], UP).set_run_time(2),
                subWaves[0].animate.next_to(subWaves[1], DOWN).set_run_time(2),
                lag_ratio=0.5
            )
        )
        self.play(
            subWaves.animate.shift(UP*1)
        )
        formula.next_to(subWaves, DOWN)
        self.play(Write(formula))
        self.wait(3)
        
        
class Waves(ThreeDScene):
    def construct(self):
        Ax = ThreeDAxes(x_range=[-5,30], y_range=[-6,6], z_range=[0,5])
        self.set_camera_orientation(zoom=0.5)
        
        Wave1 = Ax.plot(lambda x: math.sin(x)+math.cos(x*1.2)+math.sin(x*.7), color=WHITE)
        
        subWave0 = Ax.plot(lambda x: math.sin(x))
        subWave1 = Ax.plot(lambda x: math.cos(x*1.2))
        subWave2 = Ax.plot(lambda x: math.sin(x*.7))
        
        subWaves = VGroup(subWave0, subWave1, subWave2)
        subWaves.set_color_by_gradient(RED,YELLOW)
        
        self.play(Create(Wave1), FadeIn(Ax))
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(1)
        self.play(
            ReplacementTransform(Wave1, subWaves),
        )
        self.play(
            AnimationGroup(
                subWaves[0].animate.next_to(subWaves[2], OUT*4).set_run_time(2),
                subWaves[1].animate.next_to(subWaves[2], OUT*2).set_run_time(2),
                lag_ratio=0.5
            )
        )
        self.play(
            subWaves.animate.shift(OUT)
        )
        self.wait(3)
        