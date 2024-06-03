z#-------------------------------------------------
#
# Project created by QtCreator 2014-06-09T19:16:59
#
#-------------------------------------------------

QT       += core gui

QT += widgets

TARGET = EnrolmentReader
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
        qimagecv.cpp \
        imgwin.cpp

HEADERS  += mainwindow.h \
            imgwin.h\
            qimagecv.h

INCLUDEPATH += /media/m/Da4_depo_ssd/opencv-4.x/build/include

FORMS    += mainwindow.ui

LIBS += -LD:\\Qt\\opencv-build\\bin \
    libopencv_core249d \
    libopencv_highgui249d \
    libopencv_imgproc249d \
    libopencv_features2d249d \
    libopencv_calib3d249d

RESOURCES += \
    enrolementreader.qrc
