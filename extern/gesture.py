import math
from enum import IntEnum

import cv2
import mediapipe as mp
import pyautogui
from google.protobuf.json_format import MessageToDict

pyautogui.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Gesture Encodings
class Gest(IntEnum):
    # Binary Encoded
    """
    Enum for mapping all hand gesture to binary number.
    """

    FIST = 0
    PINKY = 1
    RING = 2
    MID = 4
    LAST3 = 7
    INDEX = 8
    FIRST2 = 12
    LAST4 = 15
    THUMB = 16
    PALM = 31

    # Extra Mappings
    V_GEST = 33
    TWO_FINGER_CLOSED = 34
    PINCH_MAJOR = 35
    PINCH_MINOR = 36


# Multi-handedness Labels
class HLabel(IntEnum):
    MINOR = 0
    MAJOR = 1


# Convert Mediapipe Landmarks to recognizable Gestures
class HandRecog:
    """
    Convert Mediapipe Landmarks to recognizable Gestures.
    """

    def __init__(self, hand_label):
        """
        Constructs all the necessary attributes for the HandRecog object.

        Parameters
        ----------
            finger : int
                Represent gesture corresponding to Enum 'Gest',
                stores computed gesture for current frame.
            ori_gesture : int
                Represent gesture corresponding to Enum 'Gest',
                stores gesture being used.
            prev_gesture : int
                Represent gesture corresponding to Enum 'Gest',
                stores gesture computed for previous frame.
            frame_count : int
                total no. of frames since 'ori_gesture' is updated.
            hand_result : Object
                Landmarks obtained from mediapipe.
            hand_label : int
                Represents multi-handedness corresponding to Enum 'HLabel'.
        """

        self.finger = 0
        self.ori_gesture = Gest.PALM
        self.prev_gesture = Gest.PALM
        self.frame_count = 0
        self.hand_result = None
        self.hand_label = hand_label

    def update_hand_result(self, hand_result):
        self.hand_result = hand_result

    def get_signed_dist(self, point):
        """
        returns signed euclidean distance between 'point'.

        Parameters
        ----------
        point : list contaning two elements of type list/tuple which represents
            landmark point.

        Returns
        -------
        float
        """
        sign = -1
        if (
            self.hand_result.landmark[point[0]].y
            < self.hand_result.landmark[point[1]].y
        ):
            sign = 1
        dist = (
            self.hand_result.landmark[point[0]].x
            - self.hand_result.landmark[point[1]].x
        ) ** 2
        dist += (
            self.hand_result.landmark[point[0]].y
            - self.hand_result.landmark[point[1]].y
        ) ** 2
        dist = math.sqrt(dist)
        return dist * sign

    def get_dist(self, point):
        """
        returns euclidean distance between 'point'.

        Parameters
        ----------
        point : list contaning two elements of type list/tuple which represents
            landmark point.

        Returns
        -------
        float
        """
        dist = (
            self.hand_result.landmark[point[0]].x
            - self.hand_result.landmark[point[1]].x
        ) ** 2
        dist += (
            self.hand_result.landmark[point[0]].y
            - self.hand_result.landmark[point[1]].y
        ) ** 2
        dist = math.sqrt(dist)
        return dist

    def get_dz(self, point):
        """
        returns absolute difference on z-axis between 'point'.

        Parameters
        ----------
        point : list contaning two elements of type list/tuple which represents
            landmark point.

        Returns
        -------
        float
        """
        return abs(
            self.hand_result.landmark[point[0]].z
            - self.hand_result.landmark[point[1]].z
        )

    # Function to find Gesture Encoding using current finger_state.
    # Finger_state: 1 if finger is open, else 0
    def set_finger_state(self):
        """
        set 'finger' by computing ratio of distance between finger tip
        , middle knuckle, base knuckle.

        Returns
        -------
        None
        """
        if self.hand_result == None:
            return

        points = [[8, 5, 0], [12, 9, 0], [16, 13, 0], [20, 17, 0]]
        self.finger = 0
        self.finger = self.finger | 0  # thumb
        for idx, point in enumerate(points):

            dist = self.get_signed_dist(point[:2])
            dist2 = self.get_signed_dist(point[1:])

            try:
                ratio = round(dist / dist2, 1)
            except:
                ratio = round(dist / 0.01, 1)

            self.finger = self.finger << 1
            if ratio > 0.5:
                self.finger = self.finger | 1

    # Handling Fluctations due to noise
    def get_gesture(self):
        """
        returns int representing gesture corresponding to Enum 'Gest'.
        sets 'frame_count', 'ori_gesture', 'prev_gesture',
        handles fluctations due to noise.

        Returns
        -------
        int
        """
        if self.hand_result == None:
            return Gest.PALM

        current_gesture = Gest.PALM
        if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
            if self.hand_label == HLabel.MINOR:
                current_gesture = Gest.PINCH_MINOR
            else:
                current_gesture = Gest.PINCH_MAJOR

        elif Gest.FIRST2 == self.finger:
            point = [[8, 12], [5, 9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1 / dist2
            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8, 12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID

        else:
            current_gesture = self.finger

        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0

        self.prev_gesture = current_gesture

        if self.frame_count > 4:
            self.ori_gesture = current_gesture
        return self.ori_gesture


class GestureController:
    """
    Executes commands according to detected gestures.

    Attributes
    ----------
    tx_old : int
        previous mouse location x coordinate
    ty_old : int
        previous mouse location y coordinate
    flag : bool
        true if V gesture is detected
    grabflag : bool
        true if FIST gesture is detected

    Handles camera, obtain landmarks from mediapipe, entry point
    for whole program.

    Attributes
    ----------
    gc_mode : int
        indicates weather gesture controller is running or not,
        1 if running, otherwise 0.
    cap : Object
        object obtained from cv2, for capturing video frame.
    CAM_HEIGHT : int
        highet in pixels of obtained frame from camera.
    CAM_WIDTH : int
        width in pixels of obtained frame from camera.
    hr_major : Object of 'HandRecog'
        object representing major hand.
    hr_minor : Object of 'HandRecog'
        object representing minor hand.
    dom_hand : bool
        True if right hand is domaniant hand, otherwise False.
        default True.
    """

    tx_old = 0
    ty_old = 0
    trial = True
    flag = False
    grabflag = False
    pinchmajorflag = False
    pinchminorflag = False
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 0.3
    gc_mode = 0
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None
    hr_major = None  # Right Hand by default
    hr_minor = None  # Left hand by default
    dom_hand = True

    Nothing = 0
    Moving = 1
    Click = 2
    possible_gesture = Gest

    def __init__(self, screen_size: tuple[int, int]):
        """Initilaizes attributes."""
        self.screen_size = screen_size
        self.mouse_pos = (screen_size[0] // 2, screen_size[1] // 2)
        self.action = self.Nothing
        self.gc_mode = 1
        self.cap = cv2.VideoCapture(0)
        self.CAM_HEIGHT = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.CAM_WIDTH = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.handmajor = HandRecog(HLabel.MAJOR)
        self.handminor = HandRecog(HLabel.MINOR)
        self.hands = mp_hands.Hands(
            max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.action = "state"

    def get_position(self, hand_result):
        """
        returns coordinates of current hand position.

        Locates hand to get cursor position also stabilize cursor by
        dampening jerky motion of hand.

        Returns
        -------
        tuple(float, float)
        """
        point = 9
        position = [hand_result.landmark[point].x, hand_result.landmark[point].y]
        sx, sy = self.screen_size  # size of the screen x and y
        x_mid, ymid = sx // 2, sy // 2
        x_old, y_old = self.mouse_pos  # mouse cursor position
        x = int(position[0] * sx)
        y = int(position[1] * sy)
        if self.prev_hand is None:
            self.prev_hand = x, y
        delta_x = x - self.prev_hand[0]
        delta_y = y - self.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        self.prev_hand = [x, y]

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1 / 2))
        else:
            ratio = 2.1
        x, y = x_old + delta_x * ratio, y_old + delta_y * ratio
        self.mouse_pos = (x, y)

    def get_hand_movement(self, hand_result):
        point = 9
        position = hand_result.landmark[point].x
        prev_position = self.prev_position

        if prev_position is None:
            self.prev_position = position
            return "none"

        delta = position - prev_position

        if delta < -0.5:
            self.prev_position = position
            print("left")
            return "left"
        elif delta > 0.5:
            self.prev_position = position
            print("right")
            return "right"
        else:
            print("none")
            return "none"

    def handle_controls(self, gesture, hand_result):
        """Impliments all gesture functionality."""

        # Reset grabflag
        if gesture != self.possible_gesture.FIST and self.grabflag:
            self.grabflag = False

        # Action associated with click
        if gesture == self.possible_gesture.FIST:
            if not self.grabflag:
                self.action = self.Click
                self.grabflag = True

        # Action associated with moving the hand
        elif gesture == self.possible_gesture.V_GEST:
            self.action = self.Moving

        # Default action
        else:
            self.action = self.Nothing

        # # flag reset
        # if gesture != Gest.FIST and self.grabflag:
        #     self.grabflag = False
        #     self.action = "click left"
        #     pyautogui.mouseUp(button="left")

        # # implementation
        # if gesture == Gest.V_GEST:
        #     self.flag = True
        #     self.action = "move"
        #     self.get_hand_movement(hand_result)

        # elif gesture == Gest.FIST:
        #     if not self.grabflag:
        #         self.grabflag = True
        #         pyautogui.click(button="left")
        #     # pyautogui.moveTo(x, y, duration = 0.1)

        # Merge this class with GestureController
        # either return or have the mouse position as variables

    def classify_hands(self, results):
        """
        sets 'hr_major', 'hr_minor' based on classification(left, right) of
        hand obtained from mediapipe, uses 'dom_hand' to decide major and
        minor hand.
        """
        left, right = None, None
        try:
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict["classification"][0]["label"] == "Right":
                right = results.multi_hand_landmarks[0]
            else:
                left = results.multi_hand_landmarks[0]
        except:
            pass

        try:
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict["classification"][0]["label"] == "Right":
                right = results.multi_hand_landmarks[1]
            else:
                left = results.multi_hand_landmarks[1]
        except:
            pass

        if self.dom_hand == True:
            self.hr_major = right
            self.hr_minor = left
        else:
            self.hr_major = left
            self.hr_minor = right
