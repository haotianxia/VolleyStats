# VolleyStats: A Modification of Ball Tracking in Volleyball

This study is based on [Ball tracking in volleyball](https://towardsdatascience.com/ball-tracking-in-volleyball-with-opencv-and-tensorflow-3d6e857bd2e7) (Github: [tprlab/vball](https://github.com/tprlab/vball)) and is a modification/extension of it. The original project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
We modified the original method for our volleyball setting path detection and classification research. 

## Requirements
- Python
- OpenCV 
- Keras with TensorFlow 

## Training Volleyball Models

The original project provides methods for training. To train more volleyball:

1. Get a video file with a game fragment.
2. Get the highest blobs: `python3 high.py`
3. Manually classify the blobs into 2 classes: (b)all/(n)ot ball.
4. Put the classified data into `vball-net/train`.
5. Navigate to `vball-net` using `cd vball-net`.
6. Run `python3 train.py`.

# Our Research and Modifications

Below are the modifications and new features we added to the original project:

## Extracting Ball Data

We created an advanced filter based on the original method to extract ball data. To use it, follow these steps:

1. In `blobber_with_encode.py`, change the directory to the folder where you want to store the ball path and picture.
2. Run `python3 blobber_with_encode.py`.

## Classifying Sets

We've added a new feature that classifies sets. To use it:

1. In `full_version_set_classifier.py`, change the directory to the folder where you stored the ball path.
2. Run `python3 full_version_set_classifier.py`.

## License

This project is also licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
