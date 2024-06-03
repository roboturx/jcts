#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setWindowTitle(DEFAULT_TITLE);
    setWindowIcon(QIcon(DEFAULT_ICON_FILE)); // Imagen Icono

    openB = new QPushButton("Open"); // Boton abrir imagen
    saveB = new QPushButton("Save"); // Boton guardar imagen
    exitB = new QPushButton("Exit"); // Boton salir

    next = new QPushButton("Next"); // Boton siguiente superficie
    forward = new QPushButton("Forward"); // Boton aterior superficie

    openB->setIcon(QIcon(QPixmap(DEFAULT_ICON_OPEN)));
    saveB->setIcon(QIcon(QPixmap(DEFAULT_ICON_SAVE)));
    exitB->setIcon(QIcon(QPixmap(DEFAULT_ICON_EXIT)));

    slthreshold = new QSlider(Qt::Horizontal) ;
    slthreshold->setRange(0,255);
    slthreshold->setValue(100);
    slthreshold->setToolTip("Threshold Blobs");
    disp = new QLCDNumber(4);
    disp->display(100);

    layPrin = new QVBoxLayout(); // Layout Principal
    layFile = new QHBoxLayout(); // Layout File
    laySize = new QVBoxLayout(); // Layout Image Size zoom
    layThreshold = new QVBoxLayout();// Layout herramientas
    layEnrolment = new QHBoxLayout(); // Layout de la matricula
    layNavB = new QHBoxLayout(); //Layout botones siguiente y anterior
    layInfo = new QVBoxLayout();// Layout herramientas
    enrolmentLabel = new QLabel(); // Label del pixmap de la matricula

    // Botones de archivo
    layFile->addWidget(openB);         // Boton abrir imagen
    layFile->addWidget(saveB);         // Boton guardar imagen
    layFile->addWidget(exitB);         // Boton salir

    // Display y slider tamaño de la Imagen
    dpSize = new QLCDNumber(4);
    dpSize->display(100);
    slSize = new QSlider(Qt::Horizontal);
    slSize->setRange(1,300);
    slSize->setValue(100);
    slSize->setToolTip("Zoom");
    laySize->addWidget(dpSize);
    laySize->addWidget(slSize);

    // Umbral de blobs y display
    layThreshold->addWidget(disp);
    layThreshold->addWidget(slthreshold);

    // PixMap del rectangulo
    layEnrolment->addWidget(enrolmentLabel);

    //Botones siguiente y anterior
    layNavB->addWidget(forward);
    layNavB->addWidget(next);

    // Status Bar
    statusBar = new QStatusBar(); // Barra de estado inferior
    statusLabel = new QLabel(this); // Label de la barra de estado

    statusBar->addPermanentWidget(statusLabel);
    layInfo->addWidget(statusBar);

    // Layouts
    layPrin->addLayout(layFile); // Añade el layout File
    layPrin->addLayout(laySize);
    layPrin->addLayout(layThreshold);
    layPrin->addLayout(layEnrolment);
    layPrin->addLayout(layNavB);
    layPrin->addLayout(layInfo);

    imgW = new ImgWin(this); // Ventana Principal de la Imagen
    mWid = new QWidget();// Widget principal central
    mWid->setLayout(layPrin);
    setCentralWidget(mWid);

    connect(slthreshold,SIGNAL(valueChanged(int)) , disp , SLOT(display(int)));
    connect(slthreshold,SIGNAL(valueChanged(int)) , this,SLOT(viewBlobs()));
    connect(slSize,SIGNAL(valueChanged(int)),imgW,SLOT(scaleImage(int))) ;
    connect(slSize,SIGNAL(valueChanged(int)),dpSize,SLOT(display(int))) ;
    connect(openB,SIGNAL(clicked()),imgW,SLOT(openFile())) ;
    connect(saveB,SIGNAL(clicked()),imgW,SLOT(saveFile())) ;
    connect(exitB,SIGNAL(clicked()),this,SLOT(close())) ;
    connect(forward,SIGNAL(clicked()),this,SLOT(subNum())) ;
    connect(next,SIGNAL(clicked()),this,SLOT(addNum())) ;
    num = 0;
    viewBlobs();
}
void MainWindow::viewBlobs(){

    src = QImage2Mat(imgW->getSImg());
    cv::Mat src_gray;

    cv::cvtColor( src, src_gray, CV_BGR2GRAY );
    cv::bitwise_not(src_gray,src_gray);
    cv::blur( src_gray, src_gray, cv::Size(3,3) );
    cv::Mat threshold_output;

    cv::vector<cv::Vec4i> hierarchy;

      /// Detect edges using Threshold
      cv::threshold( src_gray, threshold_output, slthreshold->value(), 255, cv::THRESH_BINARY );
      /// Find contours
      cv::findContours( threshold_output, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_TC89_L1, cv::Point(0, 0) );

      /// Approximate contours to polygons + get bounding rects and circles
      cv::vector<cv::vector<cv::Point> > contours_poly( contours.size() );
      cv::vector<cv::Rect> boundRect( contours.size() );
      cv::vector<cv::Point2f>center( contours.size() );
      cv::vector<float>radius( contours.size() );

      for( size_t i = 0; i < contours.size(); i++ )
         { cv::approxPolyDP( cv::Mat(contours[i]), contours_poly[i], 3, true );
           boundRect[i] = cv::boundingRect( cv::Mat(contours_poly[i]) );
           cv::minEnclosingCircle( (cv::Mat)contours_poly[i], center[i], radius[i] );
         }
    cv::RNG rng(12345);

      /// Draw polygonal contour + bonding rects + circles
      cv::Mat drawing = cv::Mat::zeros( threshold_output.size(), CV_8UC3 );

    char content[contours.size()];
      int n = 1;
     for( size_t i = 0; i < contours.size(); i++ )
         {
           cv::Scalar color = cv::Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) );
           cv::drawContours( drawing, contours_poly, i, color, 1, 8, cv::vector<cv::Vec4i>(), 0, cv::Point() );
           cv::fillPoly( drawing,contours_poly,cv::Scalar(255,255,255),1,0,cv::Point());
           cv::rectangle( drawing, boundRect[i].tl(), boundRect[i].br(), color, 2, 8, 0 );
           itoa(n,content,100);
           cv::putText(drawing,content,center[i], cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(0,255,0), 2, CV_AA);
           cv::circle( drawing, center[i], (int)radius[i], color, 2, 8, 0 );
           n++;
         }

        imgW->setMImg(Mat2QImage(drawing)); // Almacena la imagen en el la Imagen de Muestra
        imgW->getLabelImg()->setPixmap(QPixmap::fromImage(imgW->getMImg().scaledToWidth(imgW->getAnch())));//Actualiza el pixmap de muestra

        if(contours.size()>0){ // Dibuja el contorno de la imagen principal
            cv::Mat roi = QImage2Mat(imgW->getSImg());
            roi = roi(boundRect[getNum()]);
            enrolmentLabel->setPixmap(QPixmap::fromImage(Mat2QImage(roi)));
            statusLabel->setText(QString("Número de superficies: %1 \nEstas viendo la superficie %2")
                                 .arg(contours.size()).arg(getNum()+1));
        }
        else{
            statusLabel->setText(QString("Ninguna superficie detectada"));
        }
}

int MainWindow::getNum(){
    if(num >= contours.size() || num < (contours.size()-contours.size())){
        num = 0;
    }
    return num;
}

void MainWindow::addNum(){
    if(num>contours.size()){
        num = 0;
    }else{
        num++;
    }
    viewBlobs();
}
void MainWindow::subNum(){
    if(num <= 0)
        num = contours.size() -1;
    else{
        num--;
    }
    viewBlobs();
}

QImage MainWindow::Mat2QImage(cv::Mat const& src)
{
    QImage dest(src.cols, src.rows, QImage::Format_ARGB32);

      const float scale = 255.0;

      if (src.depth() == CV_8U) {
        if (src.channels() == 1) {
          for (int i = 0; i < src.rows; ++i) {
            for (int j = 0; j < src.cols; ++j) {
              int level = src.at<quint8>(i, j);
              dest.setPixel(j, i, qRgb(level, level, level));
            }
          }
        } else if (src.channels() == 3) {
          for (int i = 0; i < src.rows; ++i) {
            for (int j = 0; j < src.cols; ++j) {
              cv::Vec3b bgr = src.at<cv::Vec3b>(i, j);
              dest.setPixel(j, i, qRgb(bgr[2], bgr[1], bgr[0]));
            }
          }
        }
      } else if (src.depth() == CV_32F) {
        if (src.channels() == 1) {
          for (int i = 0; i < src.rows; ++i) {
            for (int j = 0; j < src.cols; ++j) {
              int level = scale * src.at<float>(i, j);
              dest.setPixel(j, i, qRgb(level, level, level));
            }
          }
        } else if (src.channels() == 3) {
          for (int i = 0; i < src.rows; ++i) {
            for (int j = 0; j < src.cols; ++j) {
              cv::Vec3f bgr = scale * src.at<cv::Vec3f>(i, j);
              dest.setPixel(j, i, qRgb(bgr[2], bgr[1], bgr[0]));
            }
          }
        }
      }

      return dest;
}

cv::Mat MainWindow::QImage2Mat(QImage const& src)
{
    cv::Mat mat = cv::Mat(src.height(), src.width(), CV_8UC4, (uchar*)src.bits(), src.bytesPerLine());
    cv::Mat mat2 = cv::Mat(mat.rows, mat.cols, CV_8UC3 );
    int from_to[] = { 0,0, 1,1, 2,2 };
    cv::mixChannels( &mat, 1, &mat2, 1, from_to, 3 );

    return mat2;
}
MainWindow::~MainWindow()
{
    delete ui;
}
