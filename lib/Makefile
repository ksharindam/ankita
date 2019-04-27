INCLUDES = -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui -I/usr/include/qt4
CFLAGS = -O2 -s -shared
LIBS = -lQtGui

all:
	g++ $(CFLAGS) $(INCLUDES) $(LIBS) -o ../ankita/floodfill.so floodfill.cpp

clean:
	rm ../ankita/floodfill.so
