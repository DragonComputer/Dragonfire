"""
Train the program by launching it with random parametters
"""

from tqdm import tqdm
import os


def main():
    """
    Launch the training with different parametters
    """

    # TODO: define:
    # step+noize
    # log scale instead of uniform

    # Define parametter: [min, max]
    dictParams = {
        "batchSize": [int, [1, 3]]
        "learningRate": [float, [1, 3]]
        }

    # Training multiple times with different parametters
    for i in range(10):
        # Generate the command line arguments
        trainingArgs = ""
        for keyArg, valueArg in dictParams:
            value = str(random(valueArg[0], max=valueArg[1]))
            trainingArgs += " --" + keyArg + " " + value

        # Launch the program
        os.run("main.py" + trainingArgs)

        # TODO: Save params/results ? or already inside training args ?


if __name__ == "__main__":
    main()
