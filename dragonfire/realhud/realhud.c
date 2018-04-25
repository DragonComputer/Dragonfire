#include <Python.h>
#include <gtk/gtk.h>
#include <gdk/gdkscreen.h>
#include <cairo.h>
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/extensions/shape.h>
#include <gdk/gdkx.h>

/*
 * This program shows you how to create transparent windows,
 * without any of the historical screenshot hacks. It requires
 * a modern system, with a compositing manager. I use xcompmgr
 * and the nvidia drivers with RenderAccel, and it works well.
 *
 * I'll take you through each step as we go. Minimal GTK+ knowledge is
 * assumed.
 *
 * gcc alphademo.c -o alphademo $( pkg-config --cflags --libs gtk+-2.0 )
 *
 * Ancestor of this file:
 * https://web.archive.org/web/20121027002505/http://plan99.net/~mike/files/alphademo.c
 *
 * Features added lately to this program are; animated GIF support,
 * alpha adjustment for images, click-through window support
 *
 * Usage(Python):
 * import realhud
 * realhud.load_gif("/home/mertyildiran/Downloads/example.gif")
 * realhud.play_gif(0.5, True)
 *
 * Author:
 * Mehmet Mert Yıldıran     mert.yildiran@bil.omu.edu.tr
 *
 * Special thanks to:
 * Mike Hearn               mike@plan99.net
 * Uli Schlachter           psychon@znc.in
 * Phillip Berndt           phillip.berndt@googlemail.com
 * for their indirect contributions to this program.
 */

int glob_argc;
char **glob_argv;

static void screen_changed(GtkWidget *widget, GdkScreen *old_screen, gpointer user_data);
static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer user_data);
static void clicked(GtkWindow *win, GdkEventButton *event, gpointer user_data);
static GdkPixbufAnimation *pixbuf_animation;
static GdkPixbufAnimationIter *iter;
static GtkWidget *window;

Display *dpy;
int screen;

char *imgpath;
float opacity = 1.0;
int is_click_through;

static gboolean timer(gpointer user_data)
{
    GTimeVal time;
    g_get_current_time(&time);
    gdk_pixbuf_animation_iter_advance(iter, &time);
    if (gdk_pixbuf_animation_iter_on_currently_loading_frame(iter)) {
        gtk_widget_destroy(window);
        gtk_main_quit();
        return FALSE;
    }
    g_timeout_add(gdk_pixbuf_animation_iter_get_delay_time(iter), timer, NULL);
    gtk_widget_queue_draw(window);
    return FALSE;
}

static PyObject* load_gif(PyObject* self, PyObject *args)
{
    /* parse the arguments */
    if (!PyArg_ParseTuple(args, "s", &imgpath)) {
        return NULL;
    }

    if (imgpath == NULL) {
        fprintf(stderr, "usage: see image.png\n");
        exit(1);
    }
    pixbuf_animation = gdk_pixbuf_animation_new_from_file(imgpath, NULL);

    Py_RETURN_NONE;
}

static PyObject* play_gif(PyObject* self, PyObject *args)
{
    fclose(stdout);
    fclose(stderr);
    /* get the display and the screen */
    if ((dpy = XOpenDisplay(getenv("DISPLAY"))) == 0)
    {
        fprintf(stderr, "Can't open display: %s\n", getenv("DISPLAY"));
        exit(1);
    }
    screen = DefaultScreen(dpy);

    PyObject *is_click_through_arg;
    /* parse the arguments */
    if (!PyArg_ParseTuple(args, "fO", &opacity, &is_click_through_arg)) {
        return NULL;
    }

    /* determine if it's click-through */
    is_click_through = PyObject_IsTrue(is_click_through_arg);

    /* boilerplate initialization code */
    gtk_init(&glob_argc, &glob_argv);

    GTimeVal time;
    g_get_current_time(&time);

    iter = gdk_pixbuf_animation_get_iter (pixbuf_animation, &time);
    timer(NULL);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

    gtk_window_set_title(GTK_WINDOW(window), "Alpha Demo");
    g_signal_connect(G_OBJECT(window), "delete-event", gtk_main_quit, NULL);


    /* Tell GTK+ that we want to draw the windows background ourself.
     * If we don't do this then GTK+ will clear the window to the
     * opaque theme default color, which isn't what we want.
     */
    gtk_widget_set_app_paintable(window, TRUE);

    /* We need to handle two events ourself: "expose-event" and "screen-changed".
     *
     * The X server sends us an expose event when the window becomes
     * visible on screen. It means we need to draw the contents.  On a
     * composited desktop expose is normally only sent when the window
     * is put on the screen. On a non-composited desktop it can be
     * sent whenever the window is uncovered by another.
     *
     * The screen-changed event means the display to which we are
     * drawing changed. GTK+ supports migration of running
     * applications between X servers, which might not support the
     * same features, so we need to check each time.
     */

    g_signal_connect(G_OBJECT(window), "expose-event", G_CALLBACK(expose), NULL);
    g_signal_connect(G_OBJECT(window), "screen-changed", G_CALLBACK(screen_changed), NULL);

    /* toggle title bar on click - we add the mask to tell X we are interested in this event */
    gtk_window_set_decorated(GTK_WINDOW(window), FALSE);
    gtk_widget_add_events(window, GDK_BUTTON_PRESS_MASK);
    g_signal_connect(G_OBJECT(window), "button-press-event", G_CALLBACK(clicked), NULL);

    /* initialize for the current display */
    screen_changed(window, NULL, NULL);

    /* Run the program */
    gtk_widget_show_all(window);
    gtk_main();

    Py_RETURN_NONE;
}


/* Only some X servers support alpha channels. Always have a fallback */
gboolean supports_alpha = FALSE;

static void screen_changed(GtkWidget *widget, GdkScreen *old_screen, gpointer userdata)
{
    /* To check if the display supports alpha channels, get the colormap */
    GdkScreen *screen = gtk_widget_get_screen(widget);
    GdkColormap *colormap = gdk_screen_get_rgba_colormap(screen);

    if (!colormap)
    {
        printf("Your screen does not support alpha channels!\n");
        colormap = gdk_screen_get_rgb_colormap(screen);
        supports_alpha = FALSE;
    }
    else
    {
        printf("Your screen supports alpha channels!\n");
        supports_alpha = TRUE;
    }

    /* Now we have a colormap appropriate for the screen, use it */
    gtk_widget_set_colormap(widget, colormap);
}

/* This is called when we need to draw the windows contents */
static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer userdata)
{
    cairo_t *cr = gdk_cairo_create(widget->window);
    int winw, winh;
    int imgw, imgh;
    int centerX, centerY;
    GdkPixbuf *pixbuf;

    //if (supports_alpha)
    //    cairo_set_source_rgba (cr, 1.0, 1.0, 1.0, 0.0); /* transparent */
    //else
    //    cairo_set_source_rgb (cr, 1.0, 1.0, 1.0); /* opaque white */

    /* draw the background */
    cairo_set_operator(cr, CAIRO_OPERATOR_IN);
    //cairo_paint (cr);

    /* hide the window from appearing in the task bar */
    gtk_window_set_skip_taskbar_hint(GTK_WINDOW(widget),TRUE);

    /* resize the window */
    gtk_window_get_size(GTK_WINDOW(widget), &winw, &winh);
    imgw = gdk_pixbuf_animation_get_width (pixbuf_animation);
    imgh = gdk_pixbuf_animation_get_height (pixbuf_animation);
    gtk_window_resize(GTK_WINDOW(widget), imgw, imgh);

    /* center the window */
    centerX = (XDisplayWidth(dpy, screen) / 2) - (winw / 2);
    centerY = (XDisplayHeight(dpy, screen) / 2) - (winh / 2);
    gtk_window_move(GTK_WINDOW(widget), centerX, centerY);

    /* make the window Always on Top */
    gtk_window_set_keep_above(GTK_WINDOW(widget), TRUE);

    if (is_click_through) {
        /* make the window click-through */
        Display *display = GDK_SCREEN_XDISPLAY(gdk_screen_get_default());
        unsigned long window_xid = GDK_WINDOW_XID(gtk_widget_get_window(widget));
        Region region = XCreateRegion();
        XRectangle rectangle = { 0, 0, 1, 1 };
        XUnionRectWithRegion(&rectangle, region, region);
        XShapeCombineRegion(display, window_xid, ShapeInput, 0, 0, region, ShapeSet);
        XDestroyRegion(region);
    }

    /* iterate over the frames of the animation */
    pixbuf = gdk_pixbuf_animation_iter_get_pixbuf(iter);
    //g_timeout_add(1000, pixbuf, NULL);
    gdk_cairo_set_source_pixbuf(cr, pixbuf, 0, 0);
    cairo_paint_with_alpha(cr, opacity);

    //gdk_cairo_set_source_pixbuf (cr, pixbuf, 0, 0);

    //cairo_paint (cr);

    cairo_destroy(cr);
    return FALSE;
}

static void clicked(GtkWindow *win, GdkEventButton *event, gpointer user_data)
{
    /* toggle window manager frames */
    //gtk_window_set_decorated(win, !gtk_window_get_decorated(win));
}

static PyMethodDef realhud_funcs[] = {
    {"load_gif", (PyCFunction)load_gif, METH_VARARGS, NULL},
    {"play_gif", (PyCFunction)play_gif, METH_VARARGS, NULL},
    {NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "realhud", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    realhud_funcs
};

PyMODINIT_FUNC PyInit_realhud(void) {
    return PyModule_Create(&moduledef);
}
#endif

void initrealhud(void)
{
    #if PY_MAJOR_VERSION >= 3
    PyInit_realhud();
    #else
    Py_InitModule3("realhud", realhud_funcs,
                   "Extension module example!");
    #endif
}

int main(int argc, char *argv[])
{
    glob_argc = argc;
    glob_argv = argv;

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initrealhud();
}
