from simulation import simulate_system
from integrators import system_velocity_verlet_step
from gravity import system_gravitational_accelerations
from collision import system_check_collision, estimate_system_impact_time
from state import *
from presets import solar_system
import time

if __name__ == "__main__":
    used_times = []
    year = 365 * 24 * 60 * 60
    steps = 60 * 60 * 24
    dt = year / steps
    cycles = 5
    for _ in range(cycles):
        start_time = time.time()
        simulate_system(solar_system, dt, steps, system_velocity_verlet_step, system_gravitational_accelerations, [], system_check_collision, estimate_system_impact_time, False, False)
        end_time = time.time()
        used_time = end_time - start_time
        used_times.append(used_time)
    average_used_time = 0
    for used_time in used_times:
        average_used_time = average_used_time + used_time
    average_used_time = average_used_time / len(used_times)
    divider = "=" * 45
    divider2 = "-" * 45
    print(divider)
    print(f" Benchmark Results for {cycles} Cycles".center(45))
    print(divider2)
    print(f"Average time used: {average_used_time}s")
    print(f"Average stepping rate: {steps / average_used_time} steps/s")
    print(divider)
    print(" Additional Information ".center(45))
    print(divider2)
    print(f"Body count: {len(solar_system.body_states)}")
    print(f"Simulated time: {year}")
    print(f"Steps: {steps}")
    print(f"dt: {dt}")
    print(divider)