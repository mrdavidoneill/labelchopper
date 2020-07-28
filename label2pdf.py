import dill
import os
from datetime import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import *
from PyPDF2.pdf import PageObject

class Label:
    def __init__(self, path, output_path=None, target_h=6.0, target_w=4.0):

        if not os.path.isfile(path):
            raise IOError("Cannot find file")
        self.target_w = target_w * 72
        self.target_h = target_h * 72
        self.name = "".join(os.path.basename(path).split(".")[0:-1])
        self.path = path
        self.pdf = PdfFileReader(str(path))
        self.pages = self.get_pages()

        if not output_path:
            output_path = "{}.pdf".format(datetime.now().strftime('%Y%m%d%H%M%S%f'))

        self.output_path = output_path
        self.output = self.process_pages()

    def get_pages(self):
        return [self.pdf.getPage(num) for num in range(self.pdf.getNumPages())]

    @staticmethod
    def rotate_page(page):
        pageObj = page.getObject()
        if '/Rotate' in pageObj:
            rotation = pageObj['/Rotate']
        else:
            rotation = 0
        page.rotateCounterClockwise(rotation)
        

    def process_pages(self):
        self.output = []
        for page in self.pages:
            Label.rotate_page(page)
            self.process_page(page)
        self.write_pdf()

    def process_page(self, page):
        X,Y,W,H = 0,1,2,3

        UPS = {"coordinates": (float(page.mediaBox.upperRight[X]) * 0.045,
                               float(page.mediaBox.upperRight[Y]) * 0.09,
                               float(page.mediaBox.upperRight[X]) * 0.825,
                               float(page.mediaBox.upperRight[Y]) * 0.46),
               "rotation": 90}
        FBA = {"coordinates": (float(page.mediaBox.upperRight[X]) * 0.02,
                               float(page.mediaBox.upperRight[Y]) * 0.51,
                               float(page.mediaBox.upperRight[X]) * 0.39,
                               float(page.mediaBox.upperRight[Y]) * 0.94),
               "rotation": 0}
        self.output.append(self.extract_object(page, UPS))
        self.output.append(self.extract_object(page, FBA))

    def extract_object(self, page, obj):
        L, B, R, T = 0, 1, 2, 3
        page = dill.copy(page)
        ROTATION = obj["rotation"]
        LEFT = obj["coordinates"][L]
        BOTTOM = obj["coordinates"][B]
        RIGHT = obj["coordinates"][R]
        TOP = obj["coordinates"][T]
        WIDTH = RIGHT - LEFT
        HEIGHT = TOP - BOTTOM

        if ROTATION != 0:
            target_w = self.target_h
            target_h = self.target_w
        else:
            target_h = self.target_h
            target_w = self.target_w

        factor = min((target_h / HEIGHT), (target_w / WIDTH), key=abs)
        page.scaleBy(factor)

        new_page = PageObject.createBlankPage(width=target_w, height=target_h)
        new_page.mergeTranslatedPage(page2=page, tx=-LEFT * factor, ty=-BOTTOM * factor)

        if ROTATION != 0:
            new_page.rotateClockwise(ROTATION)

        return new_page

    def write_pdf(self):
        pdf_writer = PdfFileWriter()
        metadata = {'/Producer': createStringObject(codecs.BOM_UTF16_BE + u_("Labelizer").encode('utf-16be'))}

        pdf_writer.addMetadata(metadata)

        for page in self.output:
            pdf_writer.addPage(page)

        with open(self.output_path, "wb") as output_file:
            pdf_writer.write(output_file)
