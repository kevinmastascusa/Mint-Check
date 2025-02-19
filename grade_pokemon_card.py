from mintcheck import grade_card

def grade_pokemon_card(image_path):
    """
    Grade a Pokémon card using the existing grading pipeline.
    """
    result = grade_card(image_path)
    if result:
        print("Grading Results for Pokémon Card:")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("Failed to grade the Pokémon card.")

if __name__ == "__main__":
    image_path = r"C:\Users\dlaev\mintcheck\data\synthetic_card_centered.jpg"
    grade_pokemon_card(image_path)
