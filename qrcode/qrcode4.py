import cv2
from math import ceil
import numpy as np

def clear_background(image, white_list, new_color) :
    """
    Clear background of an image based on a white list of rgb colors.
    All the colors that are not in the white list are replaced by new_color. 
    """
    w = np.array(white_list)
    mask = ~np.isin(image.reshape(-1, 3), w).all(axis=1)
    image.reshape(-1, 3)[mask] = new_color
    return image

def display(image):
    cv2.imshow("QR Code with Visualizations", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save(image, name):
    cv2.imwrite(name, image)

def chef_for_qr_code(image):
    qr_detector = cv2.QRCodeDetector()
    retval, points = qr_detector.detect(image)
    points = points.reshape(4, 2)  # Now it has shape (4, 2)

    # Draw the bounding box (for visualization)
    # cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
    return retval, points

def get_version(image,points, x_timing_row=20, viz=False):
    # Crop the QR code region using the bounding box
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
    y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))
    qr_code_region = image[y_min:y_max, x_min:x_max]

    # Convert the cropped region to grayscale and binarize it
    gray = cv2.cvtColor(qr_code_region, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Analyze the timing pattern (horizontal)
    # Extract a row of pixels from the middle of the QR code
    timing_row = binary[x_timing_row, :]

    # Count transitions between black and white pixels
    transitions = np.where(timing_row[:-1] != timing_row[1:])[0]

    module_size = transitions[0] + 1  # Number of modules = transitions + 1
    img_size = max(y_coords) - min(y_coords)
    num_modules = ceil(img_size/module_size)

    # Determine QR code version based on the number of modules
    qr_version = (num_modules - 17) // 4  # Formula: (num_modules - 17) / 4

    if viz :
        # Visualize the timing pattern
        timing_row_y = y_min + (x_timing_row)
        cv2.line(image, (x_min, timing_row_y), (x_max, timing_row_y), (255, 0, 0), 2)
        # Visualize the modules (draw grid lines)
        for i in range(num_modules + 1):
            x = x_min + int(i * module_size)
            cv2.line(image, (x, y_min), (x, y_max), (0, 0, 255), 1)
            y = y_min + int(i * module_size)
            cv2.line(image, (x_min, y), (x_max, y), (0, 0, 255), 1)
    
    return qr_version, module_size
    

def write_block(image, x, y, size, color=[0,0,0]):
    if x < 0 or y < 0 or x + size > image.shape[1] or y + size > image.shape[0]:
        raise ValueError("Les coordonnées ou la taille du bloc sont hors limites.")
    image[y:y + size, x:x + size] = color
    return image

def draw_alignment_pattern(image, version, size, padding):
    x, y = (4 * version + 9-1)*module_size+padding, (4 * version + 9-1)*module_size+padding
    image[y:y+size*5, x:x+size*5] = [0,0,0]
    image[y+size:y+size*4, x+size:x+size+size*3] = [255,255,255]
    image[y+2*size:y+size*3, x+2*size:x+size+size*2] = [0,0,0]
    return image

# Load the image
image = cv2.imread('qrcode_broken.png')

whitelist = [[0,0,0]]
white = [255,255,255]
image = clear_background(image, whitelist, white)
retval, points = chef_for_qr_code(image)
version, module_size = get_version(image, points, 20)

image = draw_alignment_pattern(image, version, module_size, 60)

save(image, "test.png")