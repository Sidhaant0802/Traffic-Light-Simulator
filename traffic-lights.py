import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Project : Traffic Light Simulator (Batch 100)")


crossroad_image = pygame.image.load("C:/Users/sid/Downloads/trafficlights/simple-fourway-intersection-vector-illustration-260nw-1903501381.webp")
crossroad_image = pygame.transform.scale(crossroad_image, (WIDTH, HEIGHT))
car_image = pygame.image.load("C:/Users/sid/Downloads/trafficlights/car.png")
car_image = pygame.transform.scale(car_image, (50, 50))


traffic_light_positions = [
    (250, 200),  # Top left
    (350, 200),  # Top right
    (250, 400),  # Bottom left
    (350, 400),  # Bottom right
]


cars = []
CAR_WIDTH, CAR_HEIGHT = 50, 50  # Car dimensions


def create_car():
    direction = random.choice(["up", "down", "left", "right"])
    if direction == "up":
        return {"pos": [random.randint(225, 375), 600], "dir": "up", "stop": False}
    elif direction == "down":
        return {"pos": [random.randint(225, 375), 0], "dir": "down", "stop": False}
    elif direction == "left":
        return {"pos": [600, random.randint(225, 375)], "dir": "left", "stop": False}
    elif direction == "right":
        return {"pos": [0, random.randint(225, 375)], "dir": "right", "stop": False}


def draw_traffic_light(x, y, state):
    pygame.draw.rect(window, (50, 50, 50), (x, y, 30, 80))
    pygame.draw.circle(window, (255, 0, 0) if state == 'red' else (50, 50, 50), (x + 15, y + 15), 10)
    pygame.draw.circle(window, (255, 255, 0) if state == 'yellow' else (50, 50, 50), (x + 15, y + 40), 10)
    pygame.draw.circle(window, (0, 255, 0) if state == 'green' else (50, 50, 50), (x + 15, y + 65), 10)


running = True
clock = pygame.time.Clock()
car_spawn_time = 0
car_spawn_interval = 2000  # 2 seconds

while running:
    current_time = pygame.time.get_ticks()


    if current_time - car_spawn_time >= car_spawn_interval:
        new_car = create_car()
        cars.append(new_car)
        car_spawn_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    window.blit(crossroad_image, (0, 0))


    lane_counts = [0, 0, 0, 0]

    for car in cars:
        x, y = car["pos"]
        direction = car["dir"]
        

        if direction == "up" and y < 400:
            lane_counts[2] += 1  # Bottom left lane
        elif direction == "down" and y > 200:
            lane_counts[0] += 1  # Top left lane
        elif direction == "left" and x > 200:
            lane_counts[1] += 1  # Top right lane
        elif direction == "right" and x < 400:
            lane_counts[3] += 1  # Bottom right lane


    max_lane_index = lane_counts.index(max(lane_counts))


    light_states = ['red', 'red', 'red', 'red']
    light_states[max_lane_index] = 'green'


    for i, pos in enumerate(traffic_light_positions):
        draw_traffic_light(pos[0], pos[1], light_states[i])


    for car in cars:
        x, y = car["pos"]
        direction = car["dir"]


        should_stop = False
        if direction == "up" and light_states[2] == "red" and y < 400:
            should_stop = True
        elif direction == "down" and light_states[0] == "red" and y > 200:
            should_stop = True
        elif direction == "left" and light_states[1] == "red" and x > 200:
            should_stop = True
        elif direction == "right" and light_states[3] == "red" and x < 400:
            should_stop = True


        if direction == "up" and y < 200:
            should_stop = False
        elif direction == "down" and y > 400:
            should_stop = False
        elif direction == "left" and x < 200:
            should_stop = False
        elif direction == "right" and x > 400:
            should_stop = False


        if direction == "up" and y > 300:
            should_stop = False
        elif direction == "down" and y < 300:
            should_stop = False
        elif direction == "left" and x < 300:
            should_stop = False
        elif direction == "right" and x > 300:
            should_stop = False


        if (direction == "up" and y <= 300) or (direction == "down" and y >= 300) or \
           (direction == "left" and x <= 300) or (direction == "right" and x >= 300):
            should_stop = False

        car["stop"] = should_stop


        if not car["stop"]:
            if direction == "up":
                car["pos"][1] -= 2
            elif direction == "down":
                car["pos"][1] += 2
            elif direction == "left":
                car["pos"][0] -= 2
            elif direction == "right":
                car["pos"][0] += 2


        if direction == "up":
            car["pos"][0] = max(225, min(375, car["pos"][0]))  # Keep x within road boundaries
        elif direction == "down":
            car["pos"][0] = max(225, min(375, car["pos"][0]))  # Keep x within road boundaries
        elif direction == "left":
            car["pos"][1] = max(225, min(375, car["pos"][1]))  # Keep y within road boundaries
        elif direction == "right":
            car["pos"][1] = max(225, min(375, car["pos"][1]))  # Keep y within road boundaries


        rotated_car = car_image
        if direction == "up":
            rotated_car = pygame.transform.rotate(car_image, 0)
        elif direction == "right":
            rotated_car = pygame.transform.rotate(car_image, -90)
        elif direction == "down":
            rotated_car = pygame.transform.rotate(car_image, 180)
        elif direction == "left":
            rotated_car = pygame.transform.rotate(car_image, 90)

        window.blit(rotated_car, car["pos"])


    cars = [car for car in cars if 0 <= car["pos"][0] <= WIDTH and 0 <= car["pos"][1] <= HEIGHT]

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
