from typing import List, Tuple

def can_cover(
    desired_dist_range: Tuple[int, int],
    desired_light_range: Tuple[int, int],
    hardware_cameras: List[Tuple[Tuple[int, int], Tuple[int, int]]]
) -> bool:
    dist_min, dist_max = desired_dist_range
    light_min, light_max = desired_light_range

    # Check each point in the desired range to see if any camera covers it
    for d in range(dist_min, dist_max + 1):
        for l in range(light_min, light_max + 1):
            if not any(dmin <= d <= dmax and lmin <= l <= lmax
                       for (dmin, dmax), (lmin, lmax) in hardware_cameras):
                return False
    return True

desired_dist = (1, 5)
desired_light = (1, 5)
hardware = [
    ((1, 3), (1, 5)),
    ((4, 5), (1, 2)),
    ((4, 5), (3, 5))
]

print(can_cover(desired_dist, desired_light, hardware))  # True
