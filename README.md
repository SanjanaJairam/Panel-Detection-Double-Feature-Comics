# Panel Detection Tool

This project is designed to extract panels from double-feature comics. The task is challenging due to the varying sizes and shapes of panels, as well as the presence of text and other non-panel elements.

The panels in a comic book are usually of different sizes and shapes. They can span across the entire page and lack clear boundaries. Given a comic image, the model should be able to recognize how many panels are present in the image.

## Features

- **Automated Panel Detection**: Utilizes the `PanelDetector` class to process images and identify panels.
- **Batch Processing**: Handles multiple images in a directory, making it suitable for large-scale datasets.
- **CSV Comparison**: Compares detected panel counts against a ground truth dataset provided in a CSV file.

## Getting Started

### Prerequisites

- Python 3.6+
- Required libraries:
  - `Pillow` (for image processing)
  - `numpy` (for numerical operations)
  - `pandas` (for CSV handling)
  
Install the dependencies with:
```bash
pip install -r requirements.txt
```

### Project Structure

- `main.py`: The main script to execute panel detection.
- `panel_detector.py`: Contains the `PanelDetector` class used for panel detection.
- `/images`: Directory containing input images.
- `data/actual_panels.csv'`: Ground truth CSV file for panel comparison.

### Usage

1. Place your images in the `/images` directory.
2. Ensure the `data.csv` file is available with the correct format for panel counts.
3. Run the script:
   ```bash
   python main.py
   ```
4. View the results, including the detected panel counts for each image.

### Output

1. Accuracy Metric: The script calculates the accuracy of the panel detection model by comparing the detected panel counts with the actual panel counts provided in actual_panels.csv.
2. Detailed Results: A dictionary mapping filenames to detected panel counts, along with logs summarizing accuracy and performance.

## Contributing

Feel free to contribute by submitting issues or pull requests. Contributions to improve detection accuracy or add new features are welcome!

## License

This project is licensed under the [MIT License](LICENSE).
