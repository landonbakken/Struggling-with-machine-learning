from concurrent.futures import ProcessPoolExecutor
import time

def task(n):
    # Simulate a CPU-intensive task
    total = 0
    for i in range(10**6):
        total += i * n
    return total

if __name__ == "__main__":
    tasks = range(10000)  # Define 10,000 tasks
    start_time = time.time()
    
    # Use a pool of workers
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(task, tasks))  # Map tasks to processes
    
    print(f"Completed in {time.time() - start_time} seconds")
