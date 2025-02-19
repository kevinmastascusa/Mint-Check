# MintCheck

MintCheck is a tool for grading trading cards, including Pokémon cards, based on various criteria such as centering, corners, edges, and surface quality.

## Setup

1. **Install Dependencies**:
    Ensure you have the required Python packages installed. You can install them using pip:
    ```sh
    pip install opencv-python-headless numpy scikit-image matplotlib
    ```

2. **Prepare Images**:
    Place the images of the cards you want to grade in the `C:\Users\dlaev\mintcheck\data` directory. Ensure the images are clear and taken from a top-down perspective.

## Getting Data

1. **Scanning or Photographing Cards**:
    - Use a high-resolution scanner or a good quality camera to capture images of your cards.
    - Ensure the card is placed on a flat surface and the image is taken from a top-down perspective.
    - Avoid shadows and reflections that might interfere with the grading process.

2. **Image Format**:
    - Save the images in a common format such as JPEG or PNG.
    - Name the images appropriately, for example, `pokemon_card.jpg`.

3. **Storing Images**:
    - Store the images in the `C:\Users\dlaev\mintcheck\data` directory.

## Generating Synthetic Test Images

1. **Run the Script**:
    Use the `generate_test_images.py` script to generate synthetic Pokémon card images with different centering offsets.

    ```sh
    python /c:/Users/dlaev/mintcheck/generate_test_images.py
    ```

2. **Check the Generated Images**:
    The generated images will be saved in the `C:\Users\dlaev\mintcheck\data` directory with names like `synthetic_card_centered.jpg`, `synthetic_card_offset1.jpg`, and `synthetic_card_offset2.jpg`.

## Grading a Pokémon Card

1. **Run the Script**:
    Use the `grade_pokemon_card.py` script to grade a Pokémon card. Make sure the image of the Pokémon card is named `pokemon_card.jpg` and placed in the `C:\Users\dlaev\mintcheck\data` directory.

    ```sh
    python /c:/Users/dlaev/mintcheck/grade_pokemon_card.py
    ```

2. **View Results**:
    The script will output the grading results, including scores for centering, corners, edges, and surface, as well as a final grade.

## Example

Here is an example of how to use the grading script:

1. Place the image of the Pokémon card in the `data` directory:
    ```
    C:\Users\dlaev\mintcheck\data\pokemon_card.jpg
    ```

2. Run the grading script:
    ```sh
    python /c:/Users/dlaev/mintcheck/grade_pokemon_card.py
    ```

3. View the results:
    ```
    Grading Results for Pokémon Card:
    Centering: 0.95
    Corners: 1.0
    Edges: 0.9
    Surface: 0.85
    Grade: 9.1
    ```

## Customization

You can customize the grading parameters and methods by modifying the `mintcheck.py` script. Adjust the thresholds, scoring methods, and other parameters to better suit your specific needs.

## Upload to GitHub

To push this project to GitHub, run the following commands in your project directory:

```sh
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/kevinmastascusa/Mint-Check.git
git push -u origin master
```

## License

This project is licensed under the MIT License.
