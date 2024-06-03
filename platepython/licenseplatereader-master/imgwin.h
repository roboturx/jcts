#ifndef IMGWIN_H
#define IMGWIN_H
#ifndef DEFAULTS
    #define DEFAULTS
    #define DEFAULT_ICON_OPEN   ":/images/icons/open.png"
    #define DEFAULT_ICON_EXIT   ":/images/icons/exit.png"
    #define DEFAULT_ICON_SAVE   ":/images/icons/save.png"
    #define DEFAULT_ICON_FILE   ":/images/icons/main.png"
    #define DEFAULT_IMG_FILE    ":/images/matricula.jpg"
    #define DEFAULT_OUTPUT_PATH	"C:/Documents and Settings/Administrator/Desktop"
    #define DEFAULT_IMAGE_PATH	"C:/Documents and Settings/Administrator/My Documents"
    #define DEFAULT_TITLE "EnrolemenReader"
#endif

#include <QWidget>
#include <QLabel>
#include <QStatusBar>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QFileDialog>
#include "qimagecv.h"
class ImgWin : public QMainWindow
{
    Q_OBJECT
public:
    explicit ImgWin(QWidget *parent = 0);
    QImage getSImg(); // Imagen principal
    QImage getMImg(); // Imagen modificada
    void setMImg(QImage img);
    int getAnch();
    QLabel * getLabelImg();
signals:

public slots:
    void scaleImage(int anch);
    void openFile();
    void saveFile();
private:
    int         anch;
    QString     fname;
    QImage      sImg,mImg;
    QLabel      *imgSL,*imgML;
    QLabel      *statusLabel;
    QStatusBar  *statusBar;
    QVBoxLayout *imgLay;
    QWidget     *widg;
};

#endif // IMGWIN_H
