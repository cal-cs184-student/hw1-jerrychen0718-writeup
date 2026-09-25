import random
import math

WIDTH = 800
HEIGHT = 800

random.seed(184)

svg = []

def add_line(x1, y1, x2, y2, color, width=1):
    svg.append(
        f'<line '
        f'x1="{x1:.2f}" y1="{y1:.2f}" '
        f'x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" '
        f'stroke-width="{width}"/>'
    )

def add_rect(x, y, width, height, color):
    svg.append(
        f'<rect '
        f'x="{x:.2f}" y="{y:.2f}" '
        f'width="{width:.2f}" height="{height:.2f}" '
        f'fill="{color}"/>'
    )


def add_polygon(points, color):
    point_string = " ".join(
        f"{x:.2f},{y:.2f}" for x, y in points
    )

    svg.append(
        f'<polygon points="{point_string}" '
        f'fill="{color}"/>'
    )


def add_diamond(x, y, size, color):
    add_polygon([(x, y - size), (x + size, y), (x, y + size), (x - size, y)], color)


def generate_willow_firework(cx, cy, radius, particles, gravity=180):

    colors = ["#F6B94A", "#FFD36A", "#FFE29A", "#FFF0C2", "#FFF8E7"]

    for i in range(particles):

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.55, 1.0) * radius

        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        segments = random.randint(14, 23)

        previous_x = cx
        previous_y = cy

        trail_color = random.choice(colors)

        for j in range(1, segments + 1):
            t = j / segments

            x = cx + vx * t
            y = (cy + vy * t + 0.5 * gravity * t * t)

            x += random.uniform(-1.0, 1.0)
            y += random.uniform(-1.0, 1.0)

            draw_segment = True

            if t > 0.62 and random.random() < 0.28:
                draw_segment = False

            if draw_segment:
                if t < 0.18:
                    line_width = 2
                else:
                    line_width = 1
                add_line(previous_x, previous_y, x, y, trail_color, line_width)

            if t > 0.35 and random.random() < 0.09:
                spark_size = random.uniform(0.8, 1.8)
                add_diamond(x, y, spark_size, random.choice(colors))

            previous_x = x
            previous_y = y

    add_diamond(cx, cy, 7, "#FFFBEA")
    add_diamond(cx, cy, 3, "#FFFFFF")


def generate_radial_firework(cx, cy, radius, particles, colors):

    for i in range(particles):
        angle = random.uniform(0, 2 * math.pi)
        length = random.uniform(radius * 0.45, radius)

        angle += random.uniform(-0.025, 0.025)

        x2 = cx + math.cos(angle) * length
        y2 = cy + math.sin(angle) * length

        color = random.choice(colors)

        start_fraction = random.uniform(0.02, 0.15)

        x1 = cx + math.cos(angle) * length * start_fraction
        y1 = cy + math.sin(angle) * length * start_fraction

        add_line(x1, y1, x2, y2, color, random.choice([1, 1, 1, 2]))

        if random.random() < 0.32:
            add_diamond(x2, y2, random.uniform(0.8, 2.0), color)

    add_diamond(cx, cy, 5, "#FFF4D0")
    add_diamond(cx, cy, 2.5, "#FFFFFF")

def generate_rocket(start_x, start_y, end_x, end_y,color):
    segments = 18

    previous_x = start_x
    previous_y = start_y

    for i in range(1, segments + 1):
        t = i / segments
        x = start_x + (end_x - start_x) * t

        x += math.sin(t * math.pi * 3) * 2
        y = start_y + (end_y - start_y) * t

        if random.random() > 0.18:
            add_line(previous_x, previous_y, x, y, color, 1)

        if random.random() < 0.18:
            add_diamond(x, y, random.uniform(0.7, 1.5), "#FFF5D6")

        previous_x = x
        previous_y = y

def generate_smoke(center_x, center_y, count):

    smoke_colors = ["#30496B", "#3D5270", "#5A526D", "#76596C", "#81636F", "#52647A"]

    for i in range(count):
        x = random.gauss(center_x, 100)
        y = random.gauss(center_y, 30)

        radius = random.uniform(12, 35)
        sides = random.randint(5, 8)

        points = []

        for j in range(sides):
            angle = (2 * math.pi * j / sides + random.uniform(-0.18, 0.18))

            r = radius * random.uniform(0.65, 1.15)

            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r

            points.append((px, py))

        add_polygon(points, random.choice(smoke_colors))

def generate_reflection(center_x, start_y, end_y, colors, spread):

    y = start_y

    while y < end_y:
        progress = ((y - start_y) / (end_y - start_y))

        current_spread = (spread * (0.3 + progress))

        x = center_x + random.uniform(-current_spread, current_spread)

        width = random.uniform(5, 18 + progress * 16)

        height = random.uniform(1.0, 3.0)

        add_rect(x - width / 2, y, width, height, random.choice(colors))

        y += random.uniform(4, 9)


def generate_person(x, ground_y, scale):
    head = 4 * scale

    add_polygon([(x, ground_y - 31 * scale), (x + head, ground_y - 27 * scale), (x, ground_y - 23 * scale), (x - head, ground_y - 27 * scale)], "#020713")
    
    add_polygon(
        [(x - 5 * scale, ground_y - 22 * scale), (x + 5 * scale, ground_y - 22 * scale), (x + 8 * scale, ground_y), (x - 8 * scale, ground_y)], "#020713")

def generate_boat():

    add_polygon([(120, 710), (250, 700), (225, 730), (145, 735)], "#020611")

    add_line(135, 710, 238, 705, "#26334A", 2)

    add_line(145, 718, 225, 713, "#101A2B", 2)

svg.append(
    f'<svg '
    f'xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" '
    f'height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}">'
)


add_rect(0, 0, WIDTH, HEIGHT, "#061A40")

add_rect(0, 320, 800, 180, "#08204A")

add_rect(0, 470, 800, 100, "#0A2146")

add_polygon([(0, 590), (70, 548), (135, 570), (210, 525), (285, 565), (360, 540), (440, 578), (520, 535), (600, 562), (680, 530), (800, 570), (800, 650), (0, 650)], "#07152D")

add_polygon([(0, 610), (95, 575), (180, 600), (260, 570), (350, 608), (440, 580), (540, 615), (630, 585), (720, 600), (800, 580), (800, 650), (0, 650)], "#041126")

generate_smoke(center_x=405, center_y=555, count=55)

generate_willow_firework(cx=485, cy=235, radius=265, particles=170,gravity=190)

generate_radial_firework(cx=305, cy=385, radius=115, particles=115, colors=["#FF334D", "#FF596D", "#FF7A78", "#FFC0A8"])

generate_radial_firework(cx=365, cy=515, radius=75, particles=75, colors=["#23E6E6", "#45FFFF", "#75FFF2", "#FFFFFF"])

generate_radial_firework(cx=425, cy=505, radius=68, particles=70,colors=["#29E8B0", "#50FFD0", "#90FFE0", "#E0FFF6"])

generate_radial_firework(cx=255, cy=520, radius=55, particles=55, colors=["#B75CFF", "#DD86FF", "#FF9BEF", "#FFF0FF"])

generate_rocket(330, 610, 320, 470, "#FFF4D6")

generate_rocket(355, 610, 370, 475, "#71FFFF")

generate_rocket(390, 610, 410, 455, "#FFFFFF")

generate_rocket(420, 610, 440, 485, "#FFD27A")

add_rect(0, 610, 800, 190, "#03142D")

add_line(0, 612, 800, 612, "#10264A", 2)

for x in range(360, 800, 18):
    
    if random.random() < 0.75:
        size = random.uniform(1.0, 2.5)

        add_diamond(x, 608 + random.uniform(-2, 2), size, random.choice(["#FFD36A", "#FFF0B0", "#FFB84D"]))

generate_reflection(305, 615, 795, ["#FF355E", "#FF6980", "#FFB29B"], 40)

generate_reflection(365, 615, 795, ["#23E6E6", "#65FFFF", "#A8FFFF"],35)

generate_reflection(425, 615, 795, ["#29E8B0", "#65FFD5", "#C0FFF0"], 35)

generate_reflection(485, 615, 795, ["#E8A83A", "#FFD36A", "#FFF0B0" ], 55)

for i in range(100):

    y = random.uniform(625, 795)
    x = random.uniform(0, 800)

    width = random.uniform(5, 30)

    add_line(x, y, x + width, y, random.choice(["#092653", "#0B2E61", "#10366B"]), 1)

add_polygon([(0, 645), (235, 650), (290, 690), (0, 705)], "#020713")

# Dock posts.
for x in [35, 90, 150, 215, 270]:
    add_rect(x, 635, 8, 95, "#01050D")

crowd_positions = [
    (18, 650, 1.00),
    (42, 651, 0.88),
    (64, 650, 1.05),
    (89, 653, 0.90),
    (113, 651, 1.08),
    (139, 653, 0.82),
    (162, 652, 1.00),
    (187, 653, 0.90),
    (211, 655, 1.05),
    (235, 658, 0.82)
]

for x, ground_y, scale in crowd_positions:
    generate_person(x, ground_y, scale)

generate_boat()


for i in range(35):

    x = random.uniform(0, 290)
    y = random.uniform(705, 795)

    add_line(
        x,
        y,
        x + random.uniform(8, 35),
        y,
        "#020A18",
        random.choice([1, 2])
    )


svg.append('</svg>')


with open("svg/competition.svg", "w") as f:
    f.write("\n".join(svg))


print("Generated competition.svg")
print(f"SVG elements generated: {len(svg)}")