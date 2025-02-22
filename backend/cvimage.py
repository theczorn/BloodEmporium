import cv2

class CVImage:
    """
    A wrapper around the cropped image.
    """
    def __init__(self, image_bgr):
        self.bgr = image_bgr
        self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2GRAY)
        self.r = cv2.split(self.bgr)[2]

    @staticmethod
    def from_path_bgr(path):
        return CVImage(cv2.imread(path, cv2.IMREAD_COLOR))

    def get_bgr(self):
        return self.bgr.copy()

    def get_gray(self):
        return self.gray.copy()

    def get_red(self):
        return self.r.copy()