import cv2
import numpy as np
from skimage import measure, feature
import matplotlib.pyplot as plt

# New: Gamma correction function
def gamma_correction(image, gamma=0.5):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def load_and_preprocess(image_path):
    """
    1) Read the image.
    2) Convert to grayscale.
    3) Possibly do some noise reduction.
    4) Apply gamma correction if image is overexposed.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Optional: denoise if needed
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    if np.mean(gray) >= 250:
        print("Image is overexposed; applying gamma correction")
        gray = gamma_correction(gray, gamma=0.5)
    return img, gray

def find_card_contour(img, gray):
    """
    1) Use Canny edge detection to find edges.
    2) Find contours and pick the one that likely corresponds to the card.
    3) Return the corner points if found.
    """
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    
    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area (descending)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Assume the largest contour is the card
    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        if len(approx) == 4:
            # Found a quadrilateral - assume it's our card
            return approx.reshape((4, 2))
    
    return None

def order_points(pts):
    """
    Helper to order corner points consistently:
    (top-left, top-right, bottom-right, bottom-left).
    """
    rect = np.zeros((4, 2), dtype="float32")
    # Sum and diff
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    
    return rect

def four_point_transform(image, pts):
    """
    Apply perspective transform to get a top-down view of the card.
    """
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Compute the width and height of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # Perspective transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

def measure_centering(warped):
    """
    Measure border widths to evaluate centering.
    Uses adaptive thresholding to better handle real card images.
    Additional debug prints and alternative thresholding options added.
    """
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    print(f"Gray mean: {np.mean(gray):.2f}, std: {np.std(gray):.2f}")
    
    # Try adaptive thresholding with current parameters
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3
    )
    plt.imshow(thresh, cmap='gray')
    plt.title('Adaptive Thresholded Image (Block=15, C=3)')
    plt.show()
    
    unique_values = np.unique(thresh)
    white_pixel_count = np.sum(thresh == 255)
    print(f"Unique thresh values: {unique_values}")
    print(f"White pixel count: {white_pixel_count}")
    
    # If no white pixels are found, try adjusting constant C to a negative value
    if white_pixel_count == 0:
        print("No white pixels detected; trying alternative threshold parameters...")
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, -2
        )
        plt.imshow(thresh, cmap='gray')
        plt.title('Adaptive Thresholded Image (Block=15, C=-2)')
        plt.show()
        unique_values = np.unique(thresh)
        white_pixel_count = np.sum(thresh == 255)
        print(f"Alternative unique thresh values: {unique_values}")
        print(f"Alternative white pixel count: {white_pixel_count}")
    
    coords = np.column_stack(np.where(thresh == 255))
    print(f"Coords shape: {coords.shape}")
    
    if coords.size == 0:
        print("No printed region found in the card.")
        return 0
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    
    print(f"Bounding box: x_min={x_min}, y_min={y_min}, x_max={x_max}, y_max={y_max}")
    print(f"Image shape: {warped.shape}")
    
    top_border = y_min
    bottom_border = warped.shape[0] - y_max
    left_border = x_min
    right_border = warped.shape[1] - x_max
    
    print(f"Top border: {top_border}, Bottom border: {bottom_border}")
    print(f"Left border: {left_border}, Right border: {right_border}")
    
    horizontal_ratio = min(left_border, right_border) / max(left_border, right_border)
    vertical_ratio = min(top_border, bottom_border) / max(top_border, bottom_border)
    
    return (horizontal_ratio + vertical_ratio) / 2

def check_corners(warped):
    """
    Check corner regions for sharpness or whitening.
    This is very approximate and you’d refine it heavily for a production system.
    """
    h, w = warped.shape[:2]
    corner_size = 20  # pixels to examine in each corner region
    
    # Top-left corner region
    tl_region = warped[0:corner_size, 0:corner_size]
    # Similarly define top-right, bottom-left, bottom-right
    # (You would examine the color distribution or detect whiteness, etc.)
    
    # This is just a placeholder
    # A real approach might compare average color in corners vs. main area
    # or detect how "rounded" the corner is by edge detection.
    return 1.0  # placeholder corner score

def check_edges(warped):
    """
    Check edges for whitening or chipping.
    In practice, you’d sample along each edge and compare color.
    """
    # Placeholder: you’d detect edges, measure color differences, etc.
    return 1.0  # placeholder edge score

def check_surface(warped):
    """
    Look for scratches or surface issues.
    Could do advanced methods (like filtering, difference from a 'pristine' template, or deep learning).
    """
    # Placeholder
    return 1.0  # placeholder surface score

def compute_final_grade(center_score, corner_score, edge_score, surface_score):
    """
    Combine sub-scores into a 1–10 scale. This is arbitrary.
    You would tune the weighting to your liking.
    """
    # Example weighting
    # Suppose each sub-score is on [0,1] scale, 1 = perfect
    # Weighted sum or something similar
    final = (0.4 * center_score +
             0.2 * corner_score +
             0.2 * edge_score +
             0.2 * surface_score)
    
    # Map [0,1] => [1,10] for a “PSA-like” scale
    final_grade = 1 + 9 * final  
    return round(final_grade, 1)

def grade_card(image_path):
    """
    Main function to run the entire pipeline on a single card image.
    """
    img, gray = load_and_preprocess(image_path)
    
    corners = find_card_contour(img, gray)
    if corners is None:
        print("Could not find a 4-corner contour. Is the card image clear?")
        return None
    
    warped = four_point_transform(img, corners)
    
    center_score = measure_centering(warped)
    corner_score = check_corners(warped)
    edge_score = check_edges(warped)
    surface_score = check_surface(warped)
    
    final_grade = compute_final_grade(center_score, corner_score, edge_score, surface_score)
    return {
        "Centering": center_score,
        "Corners": corner_score,
        "Edges": edge_score,
        "Surface": surface_score,
        "Grade": final_grade
    }

if __name__ == "__main__":
    # Use the real Pokémon card image
    image_path = r"C:\Users\dlaev\mintcheck\data\8.jpg"
    result = grade_card(image_path)
    if result:
        print("Grading Results:")
        for k, v in result.items():
            print(f"{k}: {v}")
