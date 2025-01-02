from PIL import Image
import numpy as np
import os

# Import the PanelDetector class
from panel_detector import PanelDetector

def main():
    # Create an instance of the PanelDetector class
    pd = PanelDetector()

    predicted_panels = {}

    for dirname, _, filenames in os.walk('/images'):
        for filename in filenames:
            no_of_panels = pd.detect_panels(os.path.join(dirname, filename))
            predicted_panels[filename] = no_of_panels

    actual_panels = pd.read_csv('data/actual_panels.csv')

    correct = 0
    for index, row in actual_panels.iterrows():
        if(abs(predicted_panels[row['Image file'].replace(" ","")] - row['No of Panels'])<1):
            correct += 1

    accuracy = correct/len(actual_panels)
    print(accuracy)





if __name__ == "__main__":
    main()
