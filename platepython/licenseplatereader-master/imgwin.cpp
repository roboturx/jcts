#include "imgwin.h"

ImgWin::ImgWin(QWidget *parent) :
    QMainWindow(parent)
{
    widg = new QWidget();
    imgSL = new QLabel();
    imgML = new QLabel();

    sImg.load(DEFAULT_IMG_FILE);
    mImg.load(DEFAULT_IMG_FILE); // Carga la imagen del disco
    fname = DEFAULT_IMG_FILE;

    anch = mImg.width();// Obtiene el ancho de la imagen
    imgLay = new QVBoxLayout();
    statusBar = new QStatusBar(); // Barra de estado inferior
    statusLabel = new QLabel(this); // Label de la barra de estado
    statusLabel->setText(QFileInfo(fname).absolutePath() +"/"+ QFileInfo(fname).fileName());
    statusBar->addPermanentWidget(statusLabel);

    // Carga la imagen en el layout QLabel imgL
    imgSL->setPixmap(QPixmap::fromImage(sImg));
    imgML->setPixmap(QPixmap::fromImage(mImg));// Pixmap de la imagen

    imgLay->addWidget(imgSL);//Añade el layout del pixmap imagen
    imgLay->addSpacing(10);
    imgLay->addWidget(imgML);//Añade el layout del pixmap imagen

    imgLay->addWidget(statusBar);
    widg->setLayout(imgLay); // Layout del widget
    setCentralWidget(widg); // Centra el widget
    show();
}
void ImgWin::openFile()
{
    fname = QFileDialog::getOpenFileName(this,"Open Image",DEFAULT_IMAGE_PATH,
                                         "Images (*.png *.jpg *.jpeg)") ;
    if ( fname.isEmpty() ) return ;
    sImg.load(fname);
    mImg.load(fname);
    anch = mImg.width();// Obtiene el ancho de la imagen

    imgSL->setPixmap(QPixmap::fromImage(sImg).scaledToWidth(sImg.width()));
    imgML->setPixmap(QPixmap::fromImage(mImg).scaledToWidth(mImg.width()));
    this->resize(this->sizeHint());//mImg.size());
    setWindowIcon(QIcon(fname));

    statusLabel->setText(QFileInfo(fname).absolutePath() +"/"+ QFileInfo(fname).fileName());// Actualiza el status bar Path de la imagen
}

void ImgWin::saveFile()
{
    fname = QFileDialog::getSaveFileName(this,"Save Image",fname,"Images (*.png *.jpg *.jpeg)") ;
    if ( fname.isEmpty() ) return ;
    mImg.save(fname);

}
QImage ImgWin::getSImg(){
    return sImg;
}
QImage ImgWin::getMImg(){
    return mImg;
}
void ImgWin::setMImg(QImage img){
    mImg = img;
}

QLabel * ImgWin::getLabelImg(){
    return imgML;
}
int ImgWin::getAnch(){
    return this->anch;
}
void ImgWin::scaleImage(int anch)
{
    this->anch = (sImg.width()*anch)/100;
    imgML->setPixmap(QPixmap::fromImage(mImg.scaledToWidth(this->anch)));
    imgSL->setPixmap(QPixmap::fromImage(sImg.scaledToWidth(this->anch)));
    this->resize(this->sizeHint());

}
