#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2019-2020 by Andreas Langhoff                             *
#* <andreas.langhoff@frm2.tum.de>                                          *
#* This program is free software; you can redistribute it and/or modify    *
#* it under the terms of the GNU General Public License v3 as published    *
#* by the Free Software Foundation;                                        *
# **************************************************************************


import copy
import numpy as np
import cv2 as cv
import quango.mlzgui
import quangoplus.polygon

from quango.qt import QImage, Qt,\
    QFileDialog, QPainter, QPen, QBrush, QTextCharFormat,\
    pyqtSlot


uifile = 'mlz_histogramChannel.ui'

class HistogramChannel(quango.mlzgui.MLZGuiPanel):  # also DiscreteInput
    UIFILE = uifile
    POLL_ATTRS = ['value']

    def reinit(self):
        self.image = None
        self.bZoom.setChecked(True)
        self.zoom = self.bZoom.isChecked()
        self.noredrawblack = False
        self.tf = QTextCharFormat()
        self.polylist = []
        self.polylistindex = len(self.polylist)
        self.RoicomboBox.insertItem(0, "add")
        self.writeWKT.setEnabled(False)
        self.editRoiBtn.setEnabled(False)
        self.addPolygon()
        self.RoicomboBox.currentIndexChanged.connect(self.on_roi_active_changed)
        self.ineditroi = False
        self.editRoiBtn.clicked.connect(self.on_editRoiBtn_clicked)
        self.wktText.textChanged.connect(self.on_wktText_textchanged)
        self.on_readWKT_clicked()

    def addPolygon(self):
        self.polylist.append(quangoplus.polygon.Polygon())
        index = len(self.polylist)
        self.RoicomboBox.insertItem(index, str(index))
        self.polylistindex = index
        self.RoicomboBox.setCurrentIndex(self.polylistindex)

    def removePolygon(self, index):
        i = 0
        items = len(self.polylist)
        for cur in self.polylist:
            if i == index:
                self.polylist.remove(cur)
                self.RoicomboBox.removeItem(items)
                self.wktText.setPlainText("")
                break
            i = i + 1

    def on_roi_active_changed(self, value):
        if value == 0:   # ='add'
            self.addPolygon()
        self.polylistindex = self.RoicomboBox.currentIndex()
        self.on_readWKT_clicked()
        if self.polylistindex == 1:
            self.writeWKT.setEnabled(False)
            self.editRoiBtn.setEnabled(False)
        else:
            self.writeWKT.setEnabled(True)
            self.editRoiBtn.setEnabled(True)

    @pyqtSlot()
    def on_editRoiBtn_clicked(self):
        if self.ineditroi:
            return
        height, width = self.mat.shape[:2]
        if height < 2 or width < 2:
            return
        if self.polylistindex == 1:
            return
        self.ineditroi = True
        self.polylist[self.polylistindex - 1].vertices().clear()

    def on_wktText_textchanged(self):
        if not  self.noredrawblack:
            self.noredrawblack = True
            txt = self.wktText.toPlainText()
            self.wktText.setCurrentCharFormat(self.tf)
            self.wktText.setPlainText(txt)
            self.wktText.update()

    def on_pollData(self, attrs):
        val = attrs['value'].value
        shape = self.proxy.detectorSize
        self.mat = val.reshape(shape)
        #maxindex = self.proxy.maxindexroi # for future use

        if shape[0] > 1 and shape[1] > 1:
            img = cv.normalize(np.int32(self.mat), None, 0, 255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
            #cv.normalize need an image with x and y > 1: It gives best normalization also with high counts per pixel
        else:
            img = (self.mat*255 /max(1, np.amax(val))).astype(np.uint8)
        if self.filter1.isChecked():

            #https://medium.com/@almutawakel.ali/opencv-filters-arithmetic-operations-2f4ff236d6aa
            kernel_sharpening = np.array([[-1, -1, -1],
                                          [-1, 9, -1],
                                          [-1, -1, -1]])
            img = cv.filter2D(img, -1, kernel_sharpening)

        if self.filter2.isChecked():
        #https://docs.opencv.org/3.4/d5/daf/tutorial_py_histogram_equalization.html
            clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl1 = clahe.apply(img)
            img = cl1

        #https://datacarpentry.org/image-processing/08-edge-detection/
        #   img3c = cv.merge([img,img,img])
        #   edges = cv.Canny(img3c,100,200)
        #   img = edges

        img = cv.applyColorMap(img, cv.COLORMAP_JET)
        self.image = img
        self.image = QImage(self.image.data, self.image.shape[0], self.image.shape[1], QImage.Format_RGB888).rgbSwapped()
        self.cts.setText(str(self.proxy.CountsInRoi))
        self.image_frame.repaint()

    @pyqtSlot()
    def on_writeWKT_clicked(self):
        wkt = str(self.wktText.toPlainText())
        self.proxy.RoiWKT = wkt
        if wkt != "":
            self.on_readWKT_clicked()

    @pyqtSlot()
    def on_readWKT_clicked(self):

        self.noredrawblack = True
        self.tf.setForeground(QBrush(Qt.red))
        self.wktText.setCurrentCharFormat(self.tf)
        if self.polylistindex > 0:
            self.proxy.selectedRoi = self.polylistindex - 1
        curwkt = self.proxy.RoiWKT
        self.wktText.setPlainText(curwkt)
        self.polylist[self.polylistindex - 1].readWKT(self.wktText.toPlainText())
        self.tf.setForeground(QBrush(Qt.black))
        self.noredrawblack = False
        self.wktText.update()

    @pyqtSlot()
    def on_saveBtn_clicked(self):
        if self.mat is None:
            return
        filename = QFileDialog.getSaveFileName(self, "Save Histogramm", "histogram.csv", "Text (*.csv)")
        np.savetxt(filename[0], self.mat, delimiter=',')

    # pylint: disable=unused-argument
    def paintEvent(self, event):
        img = self.image
        self.zoom = self.bZoom.isChecked()
        if img.width() > 256:
            self.zoom = False
        if self.zoom:
            img = self.image.scaledToWidth(self.image.width() * 2)
        painter = QPainter()
        painter.begin(self)

        painter.drawImage(self.image_frame.x(), self.image_frame.y(), img)

        i = 0
        for poly in self.polylist:
            if i + 1 == self.polylistindex:
                pen = QPen(Qt.red, 2)
            else:
                pen = QPen(Qt.black, 2)
            i = i + 1
            painter.setPen(pen)
            lastdp = None
            for qp in poly.vertices():
                qpz = copy.copy(qp)
                if self.zoom:
                    qpz.setX(qpz.x() * 2)
                    qpz.setY(qpz.y() * 2)

                adp = self.image_frame.mapToParent(qpz)
                if not lastdp is None:
                    painter.drawLine(lastdp, adp)
                lastdp = adp
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.ineditroi is True:
                if self.polylistindex > 1:
                    self.proxy.RoiWKT = ''
                    self.removePolygon(self.polylistindex - 1)

            #self.wktText.setPlainText("")
            self.ineditroi = False


    def mousePressEvent(self, event):
        if self.ineditroi:
            if event.button() == Qt.LeftButton:
                mpos = self.image_frame.mapFromParent(event.pos())
                zf = 1
                if self.zoom:
                    mpos /= 2
                    zf = 2

                doprint = True
                if not (mpos.x() >= 0 and mpos.x() <= self.image.width() * zf):
                    doprint = False
                if not (mpos.y() >= 0 and mpos.y() <= self.image.size().height() * zf):
                    doprint = False
                if doprint:
                    self.polylist[self.polylistindex - 1].addPoint(mpos)
                    self.update()

            if event.button() == Qt.RightButton:
                self.polylist[self.polylistindex - 1].close()
                self.ineditroi = False
                wkt = self.polylist[self.polylistindex - 1].WKT()
                self.wktText.setPlainText(wkt)
                self.update()
