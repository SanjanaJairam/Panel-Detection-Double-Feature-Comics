import cv2
import numpy as np
from skimage.segmentation import clear_border
from scipy import ndimage as ndi
from skimage.measure import find_contours

class PanelDetector:
    def __init__(self, min_size=5000):
        self.min_size = min_size

    def region_growing(self,image, seed):
        # Create a mask with the same shape as the image, initialized with zeros
        rows, cols = image.shape[:2]
        mask = np.zeros((rows, cols), np.uint8)

        # Set the seed pixel as the first element of the region
        region = [(seed[0], seed[1])]

        # Define the threshold used to include pixels in the region
        threshold = 10

        # Loop through the region and add neighboring pixels that meet the threshold criteria
        while len(region) > 0:
            # Get the next pixel from the region
            current_pixel = region.pop(0)

            # Check if the current pixel is within the image boundaries
            if current_pixel[0] < rows and current_pixel[1] < cols:
                # Check if the current pixel is not already part of the region and meets the threshold criteria
                if mask[current_pixel[0], current_pixel[1]] == 0 and np.abs(int(image[current_pixel[0], current_pixel[1]]) - int(image[seed[0], seed[1]])) < threshold:
                    # Add the current pixel to the region and set the mask value to 255 (white)
                    mask[current_pixel[0], current_pixel[1]] = 255
                    region.append((current_pixel[0] + 1, current_pixel[1]))
                    region.append((current_pixel[0] - 1, current_pixel[1]))
                    region.append((current_pixel[0], current_pixel[1] + 1))
                    region.append((current_pixel[0], current_pixel[1] - 1))

        return mask


    def detect_panels(self, image_path):

        # Load the image and convert it to grayscale
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)



        v = np.median(blur)
        sigma = 0.33
    #---- Apply automatic Canny edge detection using the computed median----
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        # Apply Canny edge detection to the thresholded image
        edges = cv2.Canny(blur, lower, upper)

        seed_point = (50, 50)
        mask = self.region_growing(gray, seed_point)


        # # Dilate the edges to remove any connections between panels
        # kernel = np.ones((5, 5), np.uint8)
        # dilated_edges = cv2.dilate(mask, kernel, iterations=3)
        #
        # segmentation = ndi.binary_fill_holes(dilated_edges)

        # Find contours in the dilated edges image
        contours = find_contours(mask, 0.5)

        # Sort the contours from left to right and top to bottom
    #     contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    #     print(len(contours))
    #     # Create a copy of the original image to draw the panel boxes on
        output_image = image.copy()

        panels = []
        # Loop through the contours and draw rectangles around them
        for contour in contours:
            min_y, min_x = np.min(contour, axis=0).astype(int)
            max_y, max_x = np.max(contour, axis=0).astype(int)

            w = abs(max_x - min_x)
            h = abs(max_y - min_y)
            y = min_y
            x = min_x

    #         # Calculate the aspect ratio of the bounding box
    #         aspect_ratio = float(w) / h

    #         print(w, h)
            # Only consider rectangles that have a reasonable aspect ratio and size
            if w > 50 and h > 50 and w * h > 5000:
                # Create a mask for the current panel and perform connected component analysis
                panel = image[min_y:max_y, min_x:max_x]
                panels.append(panel)
    #             _, labels = cv2.connectedComponentsWithStats(panel)


                # Loop through the labels and draw rectangles around the connected components
    #             for i in range(1, labels.max() + 1):
    #                 connected_component_mask = np.zeros(labels.shape, np.uint8)
    #                 connected_component_mask[labels == i] = 255
    #                 x_cc, y_cc, w_cc, h_cc = cv2.boundingRect(connected_component_mask)

    #                 # Draw a rectangle around the connected component
    #                 cv2.rectangle(output_image, (x + x_cc, y + y_cc), (x + x_cc + w_cc, y + y_cc + h_cc), (0, 255, 0), 2)

    #     plt.show('Panels',output_image)

        return len(panels)
