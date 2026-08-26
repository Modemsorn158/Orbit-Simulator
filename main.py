from scenarios import run_integrator_validation, run_orbit_examples, run_maneuver_examples, run_collision_example
import sys

if __name__ == "__main__":
    SCENARIOS = {
        "integrators": run_integrator_validation,
        "orbits": run_orbit_examples,
        "maneuvers": run_maneuver_examples,
        "collision": run_collision_example
    }
    
    if len(sys.argv) > 1:
        scenario_name = sys.argv[1].lower()
        if scenario_name in SCENARIOS:
            SCENARIOS[scenario_name]()
        else:
            print(f"Unknown scenario: '{sys.argv[1]}'\n")
            print("Valid scenarios:")
            for name in SCENARIOS:
                print(f"  - {name}")
    else:
        print("No scenario provided. Valid scenarios:")
        for name in SCENARIOS:
            print(f"  - {name}")