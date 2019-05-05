#include <vector>

typedef unsigned char uchar;
typedef unsigned int QRgb;

class Point
{
public:
    int x,y;
    Point():x(0),y(0) {};
    Point(int x, int y): x(x), y(y) {};
};

extern "C"
{
    void floodfill(uchar *data, int width, int height, int bpl, int x, int y, int rgba);
}


#define row(x) ((QRgb*)(data+(x)*bpl))

void floodfill(uchar *data, int w, int h, int bpl, int x, int y, int rgba)
{
    QRgb newColor = QRgb(rgba);
    QRgb oldColor = row(y)[x];//(data+i*bpl)[j];
    if  (oldColor == newColor) return;
    std::vector<Point> q;
    bool spanAbove, spanBelow;

    q.push_back(Point(x, y));

    while(!q.empty())
    {
        Point pt = q.back();
        q.pop_back();
        x = pt.x;
        y = pt.y;
        while (x >= 0 && row(y)[x] == oldColor) x--;
        x++;
        spanAbove = spanBelow = 0;
        while (x < w && row(y)[x] == oldColor )
        {
            row(y)[x] = newColor;
            if(!spanAbove && y > 0 && row(y-1)[x] == oldColor)
            {
                q.push_back(Point(x, y-1));
                spanAbove = 1;
            }
            else if (spanAbove && y > 0 && row(y-1)[x] != oldColor)
            {
                spanAbove = 0;
            }
            if(!spanBelow && y < h-1 && row(y+1)[x] == oldColor)
            {
                q.push_back(Point(x, y+1));
                spanBelow = 1;
            }
            else if(spanBelow && y < h-1 && row(y+1)[x] != oldColor)
            {
                spanBelow = 0;
            }
            x++;
        }
    }
}
