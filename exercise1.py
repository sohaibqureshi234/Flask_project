tasks = []

def add_task(name):
    tasks.append(name)
    print(f"Task '{name}' added!")

add_task("Learn Python")
add_task("Build Flask API")

print("All tasks:")
for task in tasks:
    print("-", task)