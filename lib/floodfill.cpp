#include <QImage>
#include <vector>

extern "C"
{
    void floodfill(uchar * c, int width, int height, int bpl, int x, int y, int rgba);
}
void floodFill(QImage &img, int x, int y, QRgb newColor);


void floodfill(uchar * c, int width, int height, int bpl, int x, int y, int rgba)
{
    QImage image(c, width, height, bpl, QImage::Format_ARGB32);
    floodFill(image, x, y, QRgb(rgba));
}


void
floodFill(QImage &img, int x, int y, QRgb newColor)
{
    QRgb oldColor = img.pixel(x,y);
    if (oldColor == newColor) return;
    int w = img.width();
    int h = img.height();
    std::vector<QPoint> q;
    bool spanAbove, spanBelow;

    q.push_back(QPoint(x, y));

    while(!q.empty())
    {
        QPoint pt = q.back();
        q.pop_back();
        x = pt.x();
        y = pt.y();
        while (x >= 0 && img.pixel(x,y) == oldColor) x--;
        x++;
        spanAbove = spanBelow = 0;
        while (x < w && img.pixel(x,y) == oldColor )
        {
            img.setPixel(x,y, newColor);
            if(!spanAbove && y > 0 && img.pixel(x,y-1) == oldColor)
            {
                q.push_back(QPoint(x, y - 1));
                spanAbove = 1;
            }
            else if (spanAbove && y > 0 && img.pixel(x,y-1) != oldColor)
            {
                spanAbove = 0;
            }
            if(!spanBelow && y < h - 1 && img.pixel(x,y+1) == oldColor)
            {
                q.push_back(QPoint(x, y + 1));
                spanBelow = 1;
            }
            else if(spanBelow && y < h - 1 && img.pixel(x,y+1) != oldColor)
            {
                spanBelow = 0;
            }
            x++;
        }
    }
}
