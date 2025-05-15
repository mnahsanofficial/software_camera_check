def can_cover(sw_distance, sw_light, cameras):
    # Extract software ranges
    d_sw_min, d_sw_max = sw_distance
    l_sw_min, l_sw_max = sw_light

    # Collect all critical points on the distance axis
    points = set()
    points.add(d_sw_min)
    points.add(d_sw_max)
    for cam in cameras:
        points.add(cam[0][0])
        points.add(cam[0][1])
    sorted_points = sorted(points)

    # Generate overlapping intervals within software's distance range
    overlapping_intervals = []
    for i in range(len(sorted_points) - 1):
        start = sorted_points[i]
        end = sorted_points[i + 1]
        # Check overlap with software's distance range
        interval_start = max(start, d_sw_min)
        interval_end = min(end, d_sw_max)
        if interval_start < interval_end:
            overlapping_intervals.append((interval_start, interval_end))

    # Check each interval
    for d_start, d_end in overlapping_intervals:
        # Find cameras covering this distance interval
        covering_cams = []
        for cam in cameras:
            cam_d_min, cam_d_max = cam[0]
            if cam_d_min <= d_start and cam_d_max >= d_end:
                covering_cams.append(cam[1])
        
        # Merge light intervals from covering cameras
        light_intervals = [ (l_min, l_max) for l_min, l_max in covering_cams ]
        merged = merge_intervals(light_intervals)
        if not covers(merged, (l_sw_min, l_sw_max)):
            return False

    return True

def merge_intervals(intervals):
    if not intervals:
        return []
    # Sort intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            # Merge overlapping intervals
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    return merged

def covers(merged, target):
    target_min, target_max = target
    current_min = target_min
    for interval in merged:
        if current_min >= target_max:
            break
        if interval[0] > current_min:
            return False
        current_min = max(current_min, interval[1])
    return current_min >= target_max

# Test case where coverage is complete
sw_distance = (1, 5)
sw_light = (10, 20)
cameras = [
    ((1, 3), (10, 20)),
    ((2, 5), (15, 20)),
    ((3, 5), (10, 20))
]
print(can_cover(sw_distance, sw_light, cameras))  # Output: True
