import cv2
import numpy as np

# Define background color (BGR format)
background_color = (0, 0, 255)  # Green
# background_color = (0, 0, 255)  # Change to red for red background

# Set image dimensions
width = 640
height = 480

# Create a NumPy array filled with the background color
background = np.zeros((height, width, 3), dtype=np.uint8)
background[:] = background_color

# Display the background image
cv2.imshow("Colorful Background", background)

# Wait for a key press to close the window
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()