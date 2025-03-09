import math

#===========FUNCTIONS==============================================================================
def bisection(t_down, t_up, fn, res_end, error, i):
    i += 1

    t_new = (t_down + t_up) / 2
    res_new = fn(t_new)

    if abs(res_new - res_end) < error: # if diff. is smaller than max. error
        print("smallest radius:", t_new, "mm => radius of chart:", res_new, "mm; number of cycles:", i)
        return t_new #successful try

    elif res_new > res_end:
        return bisection(t_down, t_new, fn, res_end, error, i) # runs bisection again

    elif res_new < res_end:
        return bisection(t_new, t_up, fn, res_end, error, i) #runs bisections again

# Function for calculating the next radius in sequence
def findNext(n, r, S):
    return((2**(n + 2) * S / math.radians(angle) + r**2) ** 0.5)

# Finds greatest radius > radius of diagram
def findLast(r0):
    S = math.pi * r0**2 * (angle / 2*math.pi) #area of each cell
    r_previous = r0

    for n in range(gens):
        r_next = findNext(n, r_previous, S)
        r_previous = r_next
    return r_next #the last one - radius of chart

#============PREFERENCES===============================================================================
while True:
    gens = int(input("Number of generations of ancestors: ").strip())
    if gens > 0 and if gens == int(gens):
        gens = int(gens)
        break
    else: print("Error. Value is not greater than zero or is not integer.")

width = float(input("Width of chart: ").strip())

height = float(input("Height of chart: ").strip())

while True:
    orientation = input("Portrait or landscape orientation (P/L)? ").strip().upper()
    if orientation == "P":
        width = min(width, height)
        height = max(width, height)
        break
    elif orientation == "L":
        width = max(width, height)
        height = min(width, height)
        break
    else: print("Error. This value is not available.")

while True:
    radiusMode = input("Effective or custom radius (E/C)? ").strip().upper()
    if radiusMode == "C":
        while True:
            radius = float(input("Custom radius: ").strip())
            if radius > min(width, height) / 2:
                print("Eror. Enter a radius smaller than", width / 2, ", otherwise the chart won't be able to be drawn correctly!")
            elif radius > width / 2:
                print("Beware! Diameter is greater than the width!")
            else:
                
                break
        break
    elif radiusMode == "E":
        border = float(input("Border around the chart: ").strip())
        radius = width / 2 - border
        print("⇒ radius of chart =", radius)
        break
    else: print("Error. This value is not available.")

while True:
    angleMode = input("Effective or custom angle of diagram (E/C)? ").strip().upper()
    if angleMode == "C":
        while True:
            angle = math.radians(float(input("Custom angle of diagram [°]: ").strip()))
            if angle > 2*math.pi:
                print("Error. The given angle is greater than 360 degrees.")
            elif angle <= 0:
                print("Error. The given angle is equal or smaller than 0 degrees.")
                
            elif 2*radius <= min(width, height):
                angleE = 2*math.pi
            elif orientation == "L":
                angleE = math.pi + 2 * math.asin((height - radius) / radius)
            elif orientation == "P":
                angleE = math.acos((width / 2) / radius)

            elif angle > angleE:
                print("Beware! Custom angle is greater than effective, therefore it won't fit.")
                #response = input("Do you want to proceed any way (Y/N)?").strip().upper()
                #if response == Y:
                #    break
            else:
                break
    elif angleMode == "E":
        if 2*radius <= min(width, height) - 2*border:
            angle = 2*math.pi
        elif orientation == "L":
            angle = math.pi + 2 * math.asin((height - radius) / radius)
        elif orientation == "P":
            angle = math.acos((width / 2 - border) / radius)
        angleDeg = math.degrees(angle)
        print("⇒ angle of chart =", angle, "radians, or", angleDeg, "°")
        break
    else: print("This value is not available.")

accuracy = int(input("Accuracy of output (enter number of decimals): "))
error = 10**-accuracy

#while True:
#    conversion = input("Conversion - value or without (px:mm / N): ")
#    if conversion == "N":
#        conversion = 1
#        break
#    else:
#        conversion = float(conversion)
#    if conversion <= 0:
#        print("This value is equal or smaller than zero.")
#        input("Do you want to proceed anyway (Y/N)?").strip().upper()
#        if response == Y:
#            break
#    elif conversion > 0:
#       break
print("~~~ start processing ~~~")

#==================PROCCESSING============================================================
r_start = bisection(0, radius, findLast, radius, error, 0) #first, smallest radius
print("Start radius:", r_start)

S = math.pi * r_start**2 * (angle / 2*math.pi) #area of one cell
print("one cell's area:", S, "px")

angleOver = (angle - math.pi) / 2

rs = [round(r_start, accuracy)] #creates list of rounded radius of generations' arches
r_previous = r_start

svg = open('CirGenChart.svg', 'w')
svg.write(f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg
    xmlns="http://www.w3.org/2000/svg"
    version="1.0" width="{width}" height="{height}">
''')

#Rectangular of display area (width, height) for debugging
svg.write(f'''  <rect 
    x="{0}" 
    y="{0}" 
    width="{width}" 
    height="{height}" 
    style="fill:none; stroke:#0000ff; stroke-width:1px;" />
''')

#Height of chart itself can differs from height of SVG.
if angle <= math.pi:
    chartHeight = radius
    #chartWidth = 2 * radius * math.sin(angle / 2)
else:
    chartHeight = radius + radius * math.sin((angle - math.pi) / 2)
    #chartWidth = 2 * radius

#Center circle (of root person)
svg.write(f''' <circle
    cx="{width/2}"
    cy="{((height - chartHeight) / 2 + radius)}"
    r="{r_start}" 
    style="fill:none; stroke:#ff0000; stroke-width:2px; fill:#0000ff;" />
''')

#First two lines of root person
##Coordinates
x1C = radius - r_start * math.cos(angleOver)
x2C = radius + r_start * math.cos(angleOver)
yC = radius + r_start * math.sin(angleOver)

x1 = radius - radius * math.cos(angleOver)
x2 = radius + radius * math.cos(angleOver)
y = radius + radius * math.sin(angleOver)

svg.write(f'''  <line 
    x1="{x1}" y1="{y}" 
    x2="{x1C}" y2="{yC}" 
    style="stroke:#000000; stroke-width:2px;" />
''')
svg.write(f'''  <line 
    x1="{x2C}" y1="{yC}" 
    x2="{x2}" y2="{y}" 
    style="stroke:#000000; stroke-width:2px;" />
''')

# Loop for drawing lines and arches of other generations
for n in range(gens): # For each generation
    r_current = findNext(n, r_previous, S)

    #Arches
    x1 = radius - r_current * math.cos(angleOver)
    x2 = radius + r_current * math.cos(angleOver)
    y = radius + r_current * math.sin(angleOver)

    svg.write(f'''  <path d="M {x1},{y} 
        A {r_current},{r_current} 0 1 1 {x2},{y}" 
        style="fill:none; stroke:#000000; stroke-width:2px;" />
    ''')

    # Margins
    angleA = -angleOver
    angleN = angle / 2**(n + 1)

    for m in range(2**n): 
        angleF = angleA + angleN + 2 * m * angleN
        
        x1 = radius + radius * math.cos(angleF)
        y1 = radius - radius * math.sin(angleF)
        x2 = radius + r_previous * math.cos(angleF)
        y2 = radius - r_previous * math.sin(angleF)

        svg.write(f'''  <line
            x1="{x1}" y1="{y1}" 
            x2="{x2}" y2="{y2}" 
            style="stroke:#000000; stroke-width:2px;" />
        ''') 

    rs.append(round(r_current, accuracy))
    r_previous = r_current

svg.write(
    '</svg>'
)
svg.close()
print("SVG named CirGenChart.svg was created.")

print("List of radiuses:", rs)
print("smallest angle:", angle/(2**(gens-1)), "°; smallest cell's width:", (angle/360) * 2 * math.pi * radius / (2**(gens - 1)), "px")

