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
        self.name = ("").join(os.path.basename(path).split(".")[0:-1])
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
        label_coordinates = (float(page.mediaBox.upperRight[X]) * 0.045,
                             float(page.mediaBox.upperRight[Y]) * 0.09,
                             float(page.mediaBox.upperRight[X]) * 0.825,
                             float(page.mediaBox.upperRight[Y]) * 0.46)
        fba_coordinates = (float(page.mediaBox.upperRight[X]) * 0.02,
                           float(page.mediaBox.upperRight[Y]) * 0.51,
                           float(page.mediaBox.upperRight[X]) * 0.39,
                           float(page.mediaBox.upperRight[Y]) * 0.94)
        self.output.append(self.extract_object(page, label_coordinates, rotation=90, scale="UPS"))
        self.output.append(self.extract_object(page, fba_coordinates, scale="FBA"))


    def extract_object(self, page, coordinates, rotation=None, scale=None):
        X,Y,W,H = 0,1,2,3

        obj = dill.copy(page)
        obj.mediaBox.lowerLeft = (coordinates[X], coordinates[Y])
        obj.mediaBox.upperRight = (coordinates[W], coordinates[H])
        if rotation:
            obj.rotateClockwise(rotation)

        if scale:
            if rotation:
                target_w = self.target_h
                target_h = self.target_w
            else:
                target_h = self.target_h
                target_w = self.target_w

            w = float(obj.mediaBox.getWidth())
            h = float(obj.mediaBox.getHeight())
            factor = min((target_h / h), (target_w / w), key=abs)

            obj.scaleBy(factor)

        return obj

    def write_pdf(self):
        pdf_writer = PdfFileWriter()
        metadata = {'/Producer': createStringObject(codecs.BOM_UTF16_BE + u_("Labelizer").encode('utf-16be'))}

        pdf_writer.addMetadata(metadata)

        for page in self.output:
            # new_page = PageObject.createBlankPage(width=self.target_w, height=self.target_h)
            # new_page.mergePage(page)
            pdf_writer.addPage(page)

        with open(self.output_path, "wb") as output_file:
            pdf_writer.write(output_file)
