/*
 * realhud: show a translucent image and allow clicks through part of it.
 * Experiment with shape and shape input masks.
 */

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>    // for getenv
#include <unistd.h>    // for fork
#include <libgen.h>    // for basename
#include <time.h>      // for timezone
#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <X11/xpm.h>
#include <X11/extensions/shape.h>

Display* dpy;
int screen;
Window win;
GC gc = 0;

int XWinSize = 300;
int YWinSize = 200;

/* The boundaries we'll use for the shape mask and input mask */
int outerBound = 20;
int innerBound = 75;

/* There used to be an RGBColorType defined, but it seems to be gone. */
unsigned long light, red;

static PyObject* InitWindow(PyObject* self)
{
    XpmAttributes xpmattr;
    int rv;

    if ((dpy = XOpenDisplay(getenv("DISPLAY"))) == 0)
    {
        fprintf(stderr, "Can't open display: %s\n", getenv("DISPLAY"));
        exit(1);
    }
    screen = DefaultScreen(dpy);

    int centerX = (XDisplayWidth(dpy, screen) / 2) - (XWinSize / 2);
    int centerY = (XDisplayHeight(dpy, screen) / 2) - (YWinSize / 2);

    win = XCreateSimpleWindow(dpy, RootWindow(dpy, screen),
                              0, 0, XWinSize, YWinSize, 3,
                              WhitePixel(dpy, screen),
                              BlackPixel(dpy, screen));
    if (!win)
    {
        fprintf(stderr, "Can't create window\n");
        exit(1);
    }

    XSelectInput(dpy, win, ExposureMask | KeyPressMask | StructureNotifyMask);

    XColor color, exact;
    XAllocNamedColor(dpy,
                     DefaultColormap(dpy, screen),
                     "light green",
                     &color, &exact);
    light = color.pixel;
    XAllocNamedColor(dpy,
                     DefaultColormap(dpy, screen),
                     "red",
                     &color, &exact);
    red= color.pixel;

    XGCValues gcValues;
    gcValues.foreground = WhitePixel(dpy, screen);
    gcValues.background = BlackPixel(dpy, screen);
    gc = XCreateGC(dpy, win, GCForeground | GCBackground, &gcValues);

    XMapWindow(dpy, win);

    XMoveWindow(dpy, win, centerX, centerY);

    while (HandleEvent() >= 0)
        ;
}

Region CreateRegion(int x, int y, int w, int h) {
    Region region = XCreateRegion();
    XRectangle rectangle;
    rectangle.x = x;
    rectangle.y = y;
    rectangle.width = w;
    rectangle.height = h;
    XUnionRectWithRegion(&rectangle, region, region);

    return region;
}

Region CreateFrameRegion(int bound) {
    Region region = XCreateRegion();
    XRectangle rectangle;

    /* top */
    rectangle.x = 0;
    rectangle.y = 0;
    rectangle.width = XWinSize;
    rectangle.height = bound;
    XUnionRectWithRegion(&rectangle, region, region);

    /* bottom */
    rectangle.x = 0;
    rectangle.y = YWinSize - bound;
    rectangle.width = XWinSize;
    rectangle.height = bound;
    XUnionRectWithRegion(&rectangle, region, region);

    /* left side */
    rectangle.x = 0;
    rectangle.y = 0;
    rectangle.width = bound;
    rectangle.height = YWinSize;
    XUnionRectWithRegion(&rectangle, region, region);

    /* right side */
    rectangle.x = XWinSize - bound;
    rectangle.y = 0;
    rectangle.width = bound;
    rectangle.height = YWinSize;
    XUnionRectWithRegion(&rectangle, region, region);

    return region;
}

void Draw()
{
    int shape_event_base, shape_error_base;
    Region region, inner_region, outer_region;

    XGCValues gcValues;
    gcValues.foreground = light;
    XChangeGC(dpy, gc, GCForeground, &gcValues);
    XFillRectangle(dpy, win, gc, 0, 0, XWinSize, YWinSize);

    gcValues.foreground = red;
    XChangeGC(dpy, gc, GCForeground, &gcValues);
    XFillRectangle(dpy, win, gc, outerBound, outerBound,
                   XWinSize-outerBound*2, YWinSize-outerBound*2);

    gcValues.foreground = light;
    XChangeGC(dpy, gc, GCForeground, &gcValues);
    XFillRectangle(dpy, win, gc, innerBound, innerBound,
                   XWinSize-innerBound*2, YWinSize-innerBound*2);

    if (!XShapeQueryExtension(dpy, &shape_event_base, &shape_error_base)) {
        printf("No SHAPE extension\n");
        return;
    }

    /* Make a shaped window, a rectangle smaller than the total
     * size of the window. The rest will be transparent.
     */
    region = CreateRegion(outerBound, outerBound,
                          XWinSize-outerBound*2, YWinSize-outerBound*2);
    XShapeCombineRegion(dpy, win, ShapeBounding, 0, 0, region, ShapeSet);
    XDestroyRegion(region);

    /* Make an input region that's even smaller.
     * This window will get input inside the region;
     * outside it, input will be passed through to the window below.
    region = CreateRegion(innerBound, innerBound,
                          XWinSize-innerBound*2, YWinSize-innerBound*2);
    XShapeCombineRegion(dpy, win, ShapeInput, 0, 0, region, ShapeSet);
    XDestroyRegion(region);
     */

    /* Make an input region that's everything BUT an outer ring.
     * So in the outer ring, we get input, but inside it, it passes through.
     * This creates tons of errors.
    inner_region = CreateRegion(innerBound, innerBound,
                                XWinSize-innerBound*2, YWinSize-innerBound*2);
    outer_region = CreateRegion(0, 0, XWinSize, YWinSize);
    XXorRegion(inner_region, outer_region, region);
    //XShapeCombineRegion(dpy, win, ShapeInput, 0, 0, region, ShapeSet);
    XDestroyRegion(inner_region);
    XDestroyRegion(outer_region);
    XDestroyRegion(region);
     */

    /* Make a frame region.
     * So in the outer frame, we get input, but inside it, it passes through.
     */
    region = CreateFrameRegion(innerBound);
    XShapeCombineRegion(dpy, win, ShapeInput, 0, 0, region, ShapeSet);
    XDestroyRegion(region);
}

int HandleEvent()
{
    XEvent event;
    time_t sec;
    char buffer[20];
    KeySym keysym;
    XComposeStatus compose;

    XNextEvent(dpy, &event);
    switch (event.type)
    {
      case Expose:
      case MapNotify:
          Draw();
          break;
      case ConfigureNotify:
          XWinSize = event.xconfigure.width;
          YWinSize = event.xconfigure.height;
          //printf("ConfigureNotify: now (%d, %d)\n", XWinSize, YWinSize);
          break;
      case ReparentNotify: /* When we make the window shaped? */
      case UnmapNotify:    /* e.g. move to all desktops? */
      case NoExpose:       /* No idea what this is */
          break;
      case KeyPress:
          XLookupString(&(event.xkey), buffer, sizeof buffer,
                        &keysym, &compose);
          switch (keysym)
          {
            case XK_q:
                return -1;
            default:
                break;
          }
          break;
      default:
          printf("Unknown event: %d\n", event.type);
    }
    return 0;
}

static PyMethodDef realhud_funcs[] = {
    {"InitWindow", (PyCFunction)InitWindow, METH_NOARGS, NULL},
    {NULL}
};

void initrealhud(void)
{
    Py_InitModule3("realhud", realhud_funcs,
                   "Extension module example!");
}

int main(int argc, char** argv)
{
    //InitWindow(PyObject* self);

    while (HandleEvent() >= 0)
        ;
}
