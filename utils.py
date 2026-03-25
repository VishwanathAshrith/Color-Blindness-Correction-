import numpy as np
import cv2
from PIL import Image


class Transforms:
    """
    Holds transformation matrices.
    Simulation matrices: https://arxiv.org/pdf/1711.10662.pdf
    Correction matrices: Daltonization-style channel redistribution.
    """

    @staticmethod
    def rgb_to_lms():
        return np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]]).T

    @staticmethod
    def lms_to_rgb() -> np.ndarray:
        return np.array([[0.0809, -0.1305, 0.1167],
                         [-0.0102, 0.0540, -0.1136],
                         [-0.0004, -0.0041, 0.6935]]).T

    @staticmethod
    def lms_protanopia_sim(degree: float = 1.0) -> np.ndarray:
        return np.array([[1 - degree, 2.02344 * degree, -2.52581 * degree],
                         [0, 1, 0],
                         [0, 0, 1]]).T

    @staticmethod
    def lms_deutranopia_sim(degree: float = 1.0) -> np.ndarray:
        return np.array([[1, 0, 0],
                         [0.494207 * degree, 1 - degree, 1.24827 * degree],
                         [0, 0, 1]]).T

    @staticmethod
    def lms_tritanopia_sim(degree: float = 1.0) -> np.ndarray:
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [-0.395913 * degree, 0.801109 * degree, 1 - degree]]).T

    @staticmethod
    def hybrid_protanomaly_deuteranomaly_sim(degree_p: float = 1.0, degree_d: float = 1.0) -> np.ndarray:
        return np.array([[1 - degree_p, 2.02344 * degree_p, -2.52581 * degree_p],
                         [0.494207 * degree_d, 1 - degree_d, 1.24827 * degree_d],
                         [0, 0, 1]]).T

    # ------------------------------------------------------------------ #
    #  CORRECTION MATRICES — one per type, each visually distinct         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def protanopia_correction_matrix(degree: float = 1.0) -> np.ndarray:
        """
        Protanopia (missing red cones).
        Shift red content INTO blue: reds/warm tones turn violet/purple.
        R'=R, G'=G, B'=B + 0.9*degree*R
        """
        shift = 0.9 * degree
        return np.array([[1,     0, 0],
                         [0,     1, 0],
                         [shift, 0, 1]]).T

    @staticmethod
    def deutranopia_correction_matrix(degree: float = 1.0) -> np.ndarray:
        """
        Deutranopia (missing green cones).
        Shift green content INTO red: greens turn orange/yellow.
        R'=R + 0.9*degree*G, G'=G, B'=B
        """
        return np.array([[1,             0, 0],
                         [0.9 * degree,  1, 0],
                         [0,             0, 1]]).T

    @staticmethod
    def tritanopia_correction_matrix(degree: float = 1.0) -> np.ndarray:
        """
        Tritanopia (missing blue cones).
        Shift blue content INTO red: blues turn yellow/orange.
        R'=R + 0.7*degree*B, G'=G, B'=B*(1 - 0.7*degree)
        """
        shift = 0.7 * degree
        return np.array([[1.0,   0.0, 0.0        ],
                         [0.0,   1.0, 0.0        ],
                         [shift, 0.0, 1.0 - shift]]).T

    @staticmethod
    def hybrid_correction_matrix(degree: float = 1.0) -> np.ndarray:
        """
        Hybrid (both red and green cone deficiency).
        Strategy: shift green INTO blue AND blue INTO red.
        This gives a cyan/teal cast on greens and a warm cast on blues —
        completely distinct from protanopia (violet) and deutranopia (orange).
        R'=R + 0.6*B*degree, G'=G, B'=B + 0.6*G*degree
        """
        shift = 0.6 * degree
        return np.array([[1,     0, shift],
                         [0,     1, 0    ],
                         [0,     shift, 1]]).T


class Utils:
    @staticmethod
    def load_rgb(path):
        # .convert("RGB") drops alpha channel — fixes crash on transparent PNGs
        img_rgb = np.array(Image.open(path).convert("RGB")) / 255
        return img_rgb

    @staticmethod
    def load_lms(path):
        img_rgb = np.array(Image.open(path)) / 255
        img_lms = np.dot(img_rgb[:, :, :3], Transforms.rgb_to_lms())
        return img_lms