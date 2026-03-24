from debug.homography_tool import select_points

image_points = select_points("data/intersection.mp4")

print("Selected points:", image_points)