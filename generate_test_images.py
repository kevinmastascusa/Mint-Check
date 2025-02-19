import cv2
import numpy as np

def create_synthetic_card(image_path, centering_offset=(0, 0), border_color=(255, 255, 255), printed_margin=40):
    """
    Create a synthetic Pokémon card image with a clear, well-centered printed region.
    """
    card_width, card_height = 250, 350
    border_thickness = 10

    # Create a blank card with white border
    card = np.full((card_height + 2 * border_thickness, card_width + 2 * border_thickness, 3), border_color, dtype=np.uint8)

    # Use a light gray for the main area
    main_area = np.full((card_height, card_width, 3), (220, 220, 220), dtype=np.uint8)
    
    # Draw a dark rectangle that represents the printed region
    cv2.rectangle(main_area, (printed_margin, printed_margin), (card_width - printed_margin, card_height - printed_margin), (50, 50, 50), -1)
    
    # Add white text on top of the dark printed region
    cv2.putText(main_area, 'Pokémon', (printed_margin+10, printed_margin+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(main_area, 'HP 60', (printed_margin+10, printed_margin+70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(main_area, 'Attack', (printed_margin+10, printed_margin+110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
    
    # Apply centering offset
    x_offset = border_thickness + centering_offset[0]
    y_offset = border_thickness + centering_offset[1]
    x_offset = max(border_thickness, min(x_offset, card.shape[1] - card_width - border_thickness))
    y_offset = max(border_thickness, min(y_offset, card.shape[0] - card_height - border_thickness))
    
    # Place main area onto the card
    card[y_offset:y_offset+card_height, x_offset:x_offset+card_width] = main_area

    # Add variation to corners for realism
    corner_size = 20
    cv2.circle(card, (x_offset, y_offset), corner_size, (255, 255, 255), -1)
    cv2.circle(card, (x_offset+card_width, y_offset), corner_size, (255, 255, 255), -1)
    cv2.circle(card, (x_offset, y_offset+card_height), corner_size, (255, 255, 255), -1)
    cv2.circle(card, (x_offset+card_width, y_offset+card_height), corner_size, (255, 255, 255), -1)

    cv2.imwrite(image_path, card)

if __name__ == "__main__":
    create_synthetic_card(r"C:\Users\dlaev\mintcheck\data\synthetic_card_centered.jpg", centering_offset=(0, 0), printed_margin=40)
    create_synthetic_card(r"C:\Users\dlaev\mintcheck\data\synthetic_card_offset1.jpg", centering_offset=(5, 10), printed_margin=40)
    create_synthetic_card(r"C:\Users\dlaev\mintcheck\data\synthetic_card_offset2.jpg", centering_offset=(-5, -10), printed_margin=40)
