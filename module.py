import easyocr
import cv2


class InfoString:
    info_string = []

    def __init__(self, bbox, text):
        InfoString.info_string.append(self)
        self.tl, self.tr, self.br, self.bl = bbox
        self.id_text = text
        self.crop = None

    def truncate(self, img):
        self.crop = img[int(self.tl[1]):int(self.br[1]), int(self.tl[0]):int(self.br[0])]

    @classmethod
    def text(cls):
        global info_list
        for obj in cls.info_string:
            info_list.append(obj.id_text)


def main(filename):
    global info_list
    info_list = []
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reader = easyocr.Reader(['ru', 'en'], gpu=True)
    result = reader.readtext(gray, width_ths=2)
    for (bbox, text, _) in result:
        s = InfoString(bbox, text)
        s.truncate(gray)

        # tl - top-left, br - bottom-right
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))
        cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        cv2.putText(img, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    InfoString.text()
    return info_list, img
