from logic import Environment


environments = [
    (30, 30, 5, 0.1, 0.1, 15),
    (30, 30, 4, 0.1, 0.2, 15),
    (10, 10, 2, 0.1, 0.1, 10),
    (40, 40, 10, 0.1, 0.1, 15),
    (20, 20, 4, 0.2, 0.1, 15),
    
    (30, 30, 5, 0.1, 0.1, 30),
    (30, 30, 4, 0.1, 0.2, 30),
    (10, 10, 2, 0.1, 0.1, 30),
    (40, 40, 10, 0.1, 0.1, 30),
    (20, 20, 4, 0.2, 0.1, 30)
]

agent1 = []
agent2 = []

for env in environments:
    rows, columns, childs, dirty, obstacles, t = env

    a1 = Environment(rows, columns, childs, dirty, obstacles, t, strategy_one=True)
    a2 = Environment(rows, columns, childs, dirty, obstacles, t)

    win1 = 0
    lost1 = 0
    prom1 = 0

    win2 = 0
    lost2 = 0
    prom2 = 0

    for _ in range(30):
        a1.simulate()
        if a1.win:
            win1 += 1
        elif a1.lost:
            lost1 +=1
        prom1 += a1.dirty/a1.moment * 100

        
        a2.simulate()
        if a2.win:
            win2 += 1
        elif a2.lost:
            lost2 +=1
        prom2 += a2.dirty/a2.moment * 100

    prom1 /= 30
    prom2 /= 30

    agent1.append((win1, lost1, prom1))
    agent2.append((win2, lost2, prom2))

print(agent1)

print(agent2)