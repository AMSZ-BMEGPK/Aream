import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np

# PLOT SHAPE --------------------------------------------------------------------------------------------------------------------------------------------------------
def plot(parent, shape, coordinate_on, dimension_lines_on, transformed_coordinate_on, thickness_on, colors, angle_unit, a = 1.6, b = 0.8, d = 0.8, calculated = False, u=0, v=0, rot=0):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()
    circ = False
    right = False
    parent.fig = Figure()
    parent.canvas = FigureCanvasTkAgg(parent.fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1,padx = (10,20), pady = 20)
    parent.plotted = True

    parent.ax = parent.fig.add_subplot(111)
    parent.ax.set_aspect("equal")
    parent.fig.patch.set_facecolor(colors["secondary_color"])
    parent.ax.xaxis.set_visible(False)
    parent.ax.yaxis.set_visible(False)
    parent.ax.set_frame_on(False)
 

    if shape == "Rectangle":
        x, y, proportional = set_dimensions(a, b)
        rect_x = [-x/2, -x/2, x/2, x/2, -x/2]
        rect_y = [y/2, -y/2, -y/2, y/2, y/2]

        rect_x_th = [-x/2+0.1, -x/2+0.1, x/2-0.1, x/2-0.1, -x/2+0.1]
        rect_y_th = [y/2-0.1, -y/2+0.1, -y/2+0.1, y/2-0.1, y/2-0.1]
        
        parent.ax.plot(rect_x, rect_y, colors["draw_main"], lw=2)
        parent.ax.fill(rect_x,rect_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
            parent.ax.plot(rect_x_th, rect_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(rect_x_th,rect_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0

    elif shape == "Ellipse":
        x, y, proportional = set_dimensions(a, b)
        t = np.linspace(0, 2*np.pi, 100)
        ell_x = x/2*np.cos(t)
        ell_y = y/2*np.sin(t)

        ell_x_th = (x/2-0.1)*np.cos(t)
        ell_y_th = (y/2-0.1)*np.sin(t)

        parent.ax.plot(ell_x, ell_y, colors["draw_main"], lw=2)
        parent.ax.fill(ell_x,ell_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
            parent.ax.plot(ell_x_th, ell_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(ell_x_th,ell_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0
    elif shape == "Circle":
        t = np.linspace(0, 2*np.pi, 100)
        x = y = d = 2
        proportional = True
        circ_x = d/2*np.cos(t)
        circ_y = d/2*np.sin(t)

        circ_x_th = (d/2-0.1)*np.cos(t)
        circ_y_th = (d/2-0.1)*np.sin(t)

        circ = True

        parent.ax.plot(circ_x, circ_y, colors["draw_main"], lw=2)
        parent.ax.fill(circ_x,circ_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
            parent.ax.plot(circ_x_th, circ_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(circ_x_th,circ_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0
    elif shape == "Isosceles_triangle":
        x, y, proportional = set_dimensions(a, b)
        tri_x = [-x/2, x/2, 0, -x/2]
        tri_y = [-y/3, -y/3, y/3*2, -y/3]

        tri_x_th = [-x/2+0.175, x/2-0.175, 0, -x/2+0.175]
        tri_y_th = [-y/3+0.075, -y/3+0.075, y/3*2-0.1, -y/3+0.075]

        parent.ax.plot(tri_x, tri_y, colors["draw_main"], lw=2)
        parent.ax.fill(tri_x,tri_y,color=colors["draw_main"],alpha=0.9)
        if thickness_on == True:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
            parent.ax.plot(tri_x_th, tri_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(tri_x_th,tri_y_th,color=colors["secondary_color"])
        coordinate_displacement = y/6
    elif shape == "Right_triangle":
        x, y, proportional = set_dimensions(a, b)
        if x >= y:
            th = y/10
        else:
            th = x/10

        alpha = np.arctan(y/x)
        z = th*(1/np.sin(alpha)+1/np.tan(alpha))
        w = th/np.cos(alpha) + th*np.tan(alpha)

        tri_x = [-x/3, 2*x/3, -x/3, -x/3]
        tri_y = [-y/3, -y/3, 2*y/3, -y/3]

        tri_x_th = [-x/3+th, 2*x/3-z, -x/3+th, -x/3+th]
        tri_y_th = [-y/3+th, -y/3+th, y/3*2-w, -y/3+th]

        right = True
        
        parent.ax.plot(tri_x, tri_y, colors["draw_main"], lw=2)
        parent.ax.fill(tri_x,tri_y,color=colors["draw_main"],alpha=0.9)
        if thickness_on == True:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
            parent.ax.plot(tri_x_th, tri_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(tri_x_th,tri_y_th,color=colors["secondary_color"])
        coordinate_displacement = y/6
    elif shape == None:
        None

    if coordinate_on == True:
        coordinate_system(x, y, parent.ax, coordinate_displacement, colors)
    if dimension_lines_on == True:
        dimension_lines(x, y, parent.ax, r"$a$", r"$b$", coordinate_displacement, colors, circ, right)
    if transformed_coordinate_on == True:
        transformed_coordinate_system(x, y, parent.ax, 15, colors, angle_unit, calculated, u,v,rot)
        transformation_dimensions(x, y, parent.ax, colors,calculated)
    if shape != None:
        if proportional == False:
            parent.ax.text(-x, -y+y/8, "NEM arányos!!!", verticalalignment='center', size='large', color = colors["text_color"])
        print(x,y)
    parent.canvas.draw()

# USEFUL FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------
def set_dimensions(a, b):
    ab_rate = a/b
    if ab_rate > 3:
        x = 3
        y = 1
        proportional = False
    elif ab_rate < 0.33:
        x = 1
        y = 3
        proportional = False
    else:
        x = a
        y = b
        proportional = True
    return x, y, proportional

def dimension_lines(x, y, ax, t1, t2, e, colors, circ = False, right = False):
    transparency = 1
    color = colors['draw_tertiary']
    hw = 0.015*max(x,y)
    hl = 2*hw
    if circ == False and right == False:
        line1_x = [-x/2-max(x,y)/4, 0]
        line1_y = [y/2+e, y/2+e]
        line2_x = [-x/2-max(x,y)/4, 0]
        line2_y = [-y/2+e, -y/2+e]
        line3_x = [-x/2, -x/2]
        line3_y = [-y/2-max(x,y)/4+e, -2*e]
        line4_x = [x/2, x/2]
        line4_y = [-y/2-max(x,y)/4+e, -2*e]

        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.plot(line1_x, line1_y, color,zorder=0)
        ax.plot(line2_x, line2_y, color,zorder=0)
        ax.plot(line3_x, line3_y, color,zorder=0)
        ax.plot(line4_x, line4_y, color,zorder=0)

        ax.text(
            0, -y/2-max(x,y)/16*5+e,
            t1,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
        ax.text(
            -x/2-max(x,y)/16*5, e,
            t2,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
    elif circ == True and right == False:
        line1_x = [-1, 1]
        line1_y = [1.732, -1.732]

        ax.plot(line1_x, line1_y, color,zorder=3)
        ax.arrow(line1_x[0], line1_y[0], 0.5, -0.866, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[1], line1_y[1], -0.5, 0.866, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)

        ax.text(
            1.1, -1.4,
            "Ød",
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
        # ax.text(
        #     -x/2-x*y/16*5, e,
        #     t2,
        #     horizontalalignment='center',
        #     verticalalignment='center',
        #     size='large',
        #     color = color,
        #     alpha=transparency)
    elif right == True and circ == False:
        print('derekszog meretezes indul')
        
        line1_x = [-x/2-max(x,y)/4, -x/3]
        line1_y = [y/2+e, y/2+e]
        line2_x = [-x/2-max(x,y)/4, 0]
        line2_y = [-y/2+e, -y/2+e]
        line3_x = [-x/3, -x/3]
        line3_y = [-y/2-max(x,y)/4+e, -2*e]
        line4_x = [2*x/3, 2*x/3]
        line4_y = [-y/2-max(x,y)/4+e, -2*e]

        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.plot(line1_x, line1_y, color,zorder=0)
        ax.plot(line2_x, line2_y, color,zorder=0)
        ax.plot(line3_x, line3_y, color,zorder=0)
        ax.plot(line4_x, line4_y, color,zorder=0)

        ax.text(
            x/8, -y/2-max(x,y)/16*5+e,
            t1,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
        ax.text(
            -x/2-max(x,y)/16*5, e,
            t2,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)


    elif right == True and circ == True:
        print('NEM LEHET ILYEN')


def coordinate_system(x, y, ax, e, colors):
    color = colors['draw_secondary']
    transparency = 1
    hw = 0.015*max(x,y)
    hl = 2*hw
    ax.arrow(
        -x/2-max(x,y)/8, 0, x+max(x,y)/3, 0,
        head_width=hw,
        head_length=hl,
        fc=color, ec=color,
        length_includes_head = True,
        alpha=transparency,
        zorder=3)
    ax.arrow(
        0, -y/2-max(x,y)/8+e, 0, y+max(x,y)/3,
        head_width=hw,
        head_length=hl,
        fc=color, ec=color,
        length_includes_head = True,
        alpha=transparency,
        zorder=3)
    ax.text(
        x/2+max(x,y)/5, -max(x,y)/20,
        r"$x$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = color,
        alpha=transparency)
    ax.text(
        -max(x,y)/20, y/2+max(x,y)/5+e,
        r"$y$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = color,
        alpha=transparency)

def transformed_coordinate_system(x, y, ax, phi, colors, angle_unit, calculated = False, u=0, v=0, alpha=0):
    color = colors['draw_tertiary']
    hw = 0.015*max(x,y)
    hl = 2*hw
    if calculated == False:
        phi = phi/180*np.pi
        ar1_x = (-x*3/4)*np.cos(phi)+x/5
        ar1_y = -x*3/4*np.sin(phi)+y/5
        ar1_dx = (x*3/2)*np.cos(phi)
        ar1_dy = x*3/2*np.sin(phi)
        ar2_x = y*3/4*np.sin(phi)+x/5
        ar2_y = -y*3/4*np.cos(phi)+y/5
        ar2_dx = (-y*3/2)*np.sin(phi)
        ar2_dy = y*3/2*np.cos(phi)

        ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
        ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
        ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$x_1$", horizontalalignment='center', color = color,
                            verticalalignment='center', size='large')
        ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$y_1$", horizontalalignment='center', color = color,
                            verticalalignment='center', size='large')
    else:
        print(angle_unit)
        if angle_unit == "°":
            alpha = alpha/180*np.pi
            print("deg to rad")
            print(alpha)
        ar1_x = (-x*3/4)*np.cos(alpha)+u
        ar1_y = -x*3/4*np.sin(alpha)+v
        ar1_dx = (x*3/2)*np.cos(alpha)
        ar1_dy = x*3/2*np.sin(alpha)
        ar2_x = y*3/4*np.sin(alpha)+u
        ar2_y = -y*3/4*np.cos(alpha)+v
        ar2_dx = (-y*3/2)*np.sin(alpha)
        ar2_dy = y*3/2*np.cos(alpha)

        ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
        ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
        ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$x_1$", horizontalalignment='center', color = color,
                            verticalalignment='center', size='large')
        ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$y_1$", horizontalalignment='center', color = color,
                            verticalalignment='center', size='large')

def transformation_dimensions(x, y, ax, colors, dimensions = False):
    if dimensions == False:
        color = colors['draw_tertiary']
        transparency = 1 #0.7
        hw = 0.015*max(x,y)
        hl = 2*hw
        y_disp_x = [x/5, x]
        y_disp_y = [y/5, y/5]
        ax.plot(y_disp_x, y_disp_y, color, lw=1, zorder=5, alpha=transparency)
        ax.arrow(x/2+x/8, 0, 0, y/5,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
        ax.arrow(x/2+x/8, y/5, 0, -y/5,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
        ax.text(x/2+x/6, y/8, r"$v$", horizontalalignment='center', color = color,
                            verticalalignment='center', alpha=transparency)
        x_disp_x = [x/5, x/5]
        x_disp_y = [y/5, -y/5]
        ax.plot(x_disp_x, x_disp_y, color, lw=1, zorder=5, alpha=transparency)
        ax.arrow(0, -y/8, x/5, 0,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
        ax.arrow(x/5, -y/8, -x/5, 0,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
        ax.text(x/8, -y/12, r"$u$", horizontalalignment='center', color = color,
                        verticalalignment='center', alpha=transparency)
        style = "Simple, tail_width=0.2, head_width=4, head_length=8"
        kw = dict(arrowstyle=style, color=color)
        a3 = patches.FancyArrowPatch((x/2+x/3, y/5), (x/2+x/5+x/20, y/5+x*3/20),
                                connectionstyle="arc3,rad=.2", **kw, alpha=transparency)
        ax.add_patch(a3)
        ax.text(x/2+x/4+x/8, y/4+y/12, r"$\varphi$", horizontalalignment='center', color = color,
                        verticalalignment='center', alpha=transparency)
    else:
        None
    
def plot_principal_axes(parent, colors, ax, alpha, angle_unit, transformed_coordinate_on,shape, a = 1.6, b = 0.8, d = 0.8):
    principal_x = True
    x, y, proportional = set_dimensions(a, b)
    try:
        parent.principal_axis1.remove()
        parent.principal_axis2.remove()
        parent.principal_axis1_text.remove()
        parent.principal_axis2_text.remove()
    except:
        None
    if transformed_coordinate_on == False:
        color = colors['draw_principal']
    hw = 0.015*max(x,y)
    hl = 2*hw

    phi = alpha

    if shape == "Circle":
        ar1_x = -1.6*y*np.cos(phi)
        ar1_y = -1.6*y*np.sin(phi)
        ar1_dx = 3.2*y*np.cos(phi)
        ar1_dy = 3.2*y*np.sin(phi)
        ar2_x = 1*x*np.sin(phi)
        ar2_y = -1*x*np.cos(phi)
        ar2_dx = -2*x*np.sin(phi)
        ar2_dy = 2*x*np.cos(phi)

        ar1_x = -1.5*x / 2
        ar1_y = 0
        ar1_dx = 1.5*x
        ar1_dy = 0
        ar2_x = 0
        ar2_y = -1.5*y
        ar2_dx = 0
        ar2_dy = 3*y
    else:
        if x > y:
            ar1_x = -y/1.8*np.cos(phi)
            ar1_y = -y/1.8*np.sin(phi)
            ar1_dx = 2*0.56*y*np.cos(phi)
            ar1_dy = 2*0.56*y*np.sin(phi)
            ar2_x = x/1.8*np.sin(phi)
            ar2_y = -x/1.8*np.cos(phi)
            ar2_dx = -2*0.56*x*np.sin(phi)
            ar2_dy = 2*0.56*x*np.cos(phi)
        else:
            ar1_x = -x/1.8*np.cos(phi)
            ar1_y = -x/1.8*np.sin(phi)
            ar1_dx = 2*0.56*x*np.cos(phi)
            ar1_dy = 2*0.56*x*np.sin(phi)
            ar2_x = y/1.8*np.sin(phi)
            ar2_y = -y/1.8*np.cos(phi)
            ar2_dx = -2*0.56*y*np.sin(phi)
            ar2_dy = 2*0.56*y*np.cos(phi)


    ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
    ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
    ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$I_1$", horizontalalignment='center', color = color,
                        verticalalignment='center', size='large')
    ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$I_2$", horizontalalignment='center', color = color,
                        verticalalignment='center', size='large')

    parent.canvas.draw()