from mintcheck import grade_card

if __name__ == "__main__":
    # Use the real card image "8.jpg"
    image_path = r"C:\Users\dlaev\mintcheck\data\8.jpg"
    result = grade_card(image_path)
    if result:
        print("Grading Results for image:", image_path)
        for metric, score in result.items():
            print(f"{metric}: {score}")
    else:
        print("Failed to grade the image.")
