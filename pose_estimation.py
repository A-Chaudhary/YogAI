# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run pose classification and pose estimation."""
import argparse
import logging
import sys
import time

from data import Category
import cv2
from ml import Classifier
from ml import Movenet
import utils


def run(estimation_model: str, tracker_type: str, classification_model: str,
        label_file: str, image) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    estimation_model: Name of the TFLite pose estimation model.
    tracker_type: Type of Tracker('keypoint' or 'bounding_box').
    classification_model: Name of the TFLite pose classification model.
      (Optional)
    label_file: Path to the label file for the pose classification model. Class
      names are listed one name per line, in the same order as in the
      classification model output. See an example in the yoga_labels.txt file.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
  """
  #print(estimation_model, tracker_type, classification_model, label_file, camera_id, width, height, image)
  # Notify users that tracker is only enabled for MoveNet MultiPose model.
  if tracker_type and (estimation_model != 'movenet_multipose'):
    logging.warning(
        'No tracker will be used as tracker can only be enabled for '
        'MoveNet MultiPose model.')

  # Initialize the pose estimator selected.
  if estimation_model in ['movenet_lightning', 'movenet_thunder']:
    pose_detector = Movenet(estimation_model)
  elif estimation_model == 'posenet':
    pose_detector = Posenet(estimation_model)
  elif estimation_model == 'movenet_multipose':
    pose_detector = MoveNetMultiPose(estimation_model, tracker_type)
  else:
    sys.exit('ERROR: Model is not supported.')


  # Visualization parameters
  classification_results_to_show = 5
  keypoint_detection_threshold_for_classifier = 0.1
  classifier = None

  # Initialize the classification model
  if classification_model:
    classifier = Classifier(classification_model, label_file)
    classification_results_to_show = min(classification_results_to_show,
                                         len(classifier.pose_class_names))

  if estimation_model == 'movenet_multipose':
    # Run pose estimation using a MultiPose model.
    list_persons = pose_detector.detect(image)
  else:
    #Run pose estimation using a SinglePose model, and wrap the result in an
    # array.
    list_persons = [pose_detector.detect(image)]

  if classifier:
    person = list_persons[0]
    min_score = min([keypoint.score for keypoint in person.keypoints])
    if min_score < keypoint_detection_threshold_for_classifier:
      error_text = 'Some keypoints are not detected. Make sure the person is fully visible in the camera.'
      return error_text
    else:
      # Run pose classification
      prob_list = classifier.classify_pose(person)

      pose_dict = {}

      # Map old labels to new ones and build the dictionary
      label_map = {
          'dog': 'Downward Dog',
          'warrior': 'Warrior III',
          'cobra': 'Cobra',
          'chair': 'Chair',
          'tree': 'Tree'
      }

      for category in prob_list:
        old_label = category.label
        if old_label in label_map:
          new_label = label_map[old_label]
          pose_dict[new_label] = category.score

      return pose_dict

