#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QVBoxLayout>
#include <QSlider>
#include <QLCDNumber>
#include "imgwin.h"
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    cv::Mat     QImage2Mat(QImage const& src);
    QImage      Mat2QImage(cv::Mat const& src);
    int         getNum();
public slots:
    void addNum();
    void subNum();
    void viewBlobs();
private:
    cv::vector<cv::vector<cv::Point> > contours;
    QWidget *mWid;
    std::vector <std::vector<cv::Point2i> > blobs;
    cv::Mat         output,src,binary;
    QSlider         *slthreshold,*slSize;
    QLCDNumber      *disp,*dpSize;
    QLabel          *enrolmentLabel,*statusLabel;
    QStatusBar      *statusBar;
    ImgWin          *imgW;
    QVBoxLayout     *layPrin,*layThreshold,*laySize,*layInfo;
    QHBoxLayout     *layFile,*layEnrolment,*layNavB;
    QPushButton     *exitB, *openB, *saveB,*next,*forward;
    Ui::MainWindow  *ui;
    size_t num;
};

#endif // MAINWINDOW_H
