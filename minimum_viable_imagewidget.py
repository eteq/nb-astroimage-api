class ImageWidget:
    def __init__(self, properties...):  # all the properties below should be valid kwargs
        """
        Minimal widget does *not* have any fancy initializer parsing.  The user
        has to call a `load` method.  Future-proofing against future `load_*`
        methods so that the initializer doesn't get too confusing.
        """
    # OPTION 2 / stretch goal - I favor only option 1:
    def __init__(self, image=None, properties...):
        """
        image can be a string to be interpreted as a fits file, an HDU,
        an NDData, or a 2D array.  These would just call the `load_*` methods.
        """

    def _repr_html_(self):
        """
        This yields the actual widget itself.  That is, the user should be able
        to simply do:

            w = ImageWidget()
            w

        in a notebook and have it show the widget.
        """

    def load_fits(self, fitsorfn):
        """
        ``fitsorfn`` can be either a string (a file name) or an HDU
        (*not* an HDUList. Although that presents a subtle problem for fits
        files where some of the WCS information is in other HDUs. Might have to
        say that those require going through nddata)
        """

    def load_nddata(self, nddata):
        """
        ``nddata`` must be an nddata object.

        While the minimal version just uses the data and the wcs, future
        enhancements could include flag/masking support, etc.
        """

    def load_array(self, arr):
        """
        ``arr`` is a 2D array.  No way to provide WCS, and this is
        *intentional* - the user should create an `nddata` if they want wcs.
        """

    def center_on(self, x, y):
        """
        Centers the view on a particular point
        """

    def offset_to(self, dx, dy):
        """
        Moves the center to a point that's ``dx``/``dy`` away from the current
        center.
        """

    @property
    def zoom_level(self):
        """
        Settable, a float.  If "1", means real-pixel-size.  "2" means zoom out
        by factor of 2, 0.5 means 2 screen pixels for 1 data pixel, etc.

        Might be better as a getter/setter pair rather than property since it
        may be performance-intensive?
        """

    def zoom(self, val):
        """
        Zoom in or out by the ``val`` factor.  Presumably the "real" logic is
        shared between this and `zoom_level`.
        """

    def select_points(self):
        """
        Enter "selection mode".  This turns off ``click_drag``, and any click
        will create a mark.

        Later enhancements (second round): control the shape/size/color of the
        selection marks a la the `add_marks` enhancement
        """

    def get_selection(self):
        """
        Return the locations of points from the most recent round of
        selection mode.

        Return value should be an astropy table, with "` and "y" columns
        (or whatever the default column names are from ``add_marks``).  If WCS
        is present, should *also* have a "coords" column with a `SkyCoord`
        object.
        """

    def stop_selecting(self, clear_marks=True):
        """
        Just what it says on the tin.

        If ``clear_marks`` is False, the selected points are kept as visible
        marks until ``reset_marks`` is called.  Otherwise the marks disappear.
        ``get_selection()`` should still work even if ``clear_markers`` is
        False, up until the next ``select_points`` call happens.
        """

    def is_selecting(self):
        """
        True if in selection mode, False otherwise.
        """

    def add_marks(self, table, x_colname='x', y_colname='y', skycoord_colname='coord'):
        """
        Creates markers in the image at given points.

        Input is an astropy Table, and the column names for the x/y pixels will
        be taken from the ``xcolname`` and ``ycolname`` kwargs.  If the
        ``skycoord_colname`` is present, the table has the row, and WCS is
        present on the image, mark the positions from the skycoord.  If both
        skycoord *and* x/y columns are present, raise an error about not knowing
        which to pick.


        Later enhancements (second round): more table columns to control
        size/style/color of marks, ``remove_mark`` to remove some but not all
        of the marks, let the initial argument be a skycoord or a 2xN array.
        """

    def reset_marks(self):
        """
        Delete all marks
        """

    @property
    def stretch(self):
        """
        Settable.

        One of the stretch objects from `astropy.visualization`, or something
        that matches that API.

        Note that this is *not* the same as the

        Might be better as getter/setter rather than property since it may be
        performance-intensive?
        """

    def cuts(self):
        """
        Settable.

        One of the cut objects from `astropy.visualization`, or something
        that matches that API

        Might be better as getter/setter rather than property since it may be
        performance-intensive?
        """

    @property
    def cursor(self):
        """
        Settable.
        If True, the pixel and possibly wcs is shown in the widget (see below),
        if False, the position is not shown.

        Possible enhancement: instead of True/False, could be "top", "bottom",
        "left", "right", None/False
        """

    @property
    def click_drag(self):
        """
        Settable.
        If True, the "click-and-drag" mode is an available interaction for
        panning.  If False, it is not.

        Note that this should be automatically made `False` when selection mode
        is activated.
        """

    @property
    def click_center(self):
        """
        Settable.
        If True, middle-clicking can be used to center.  If False, that
        interaction is disabled.

        In the future this might go from True/False to being a selectable
        button. But not for the first round.
        """

    @property
    def scroll_pan(self):
        """
        Settable.
        If True, scrolling moves around in the image.  If False, scrolling
        (up/down) *zooms* the image in and out.
        """

    def save(self, filename):
        """
        Save out the current image view to an on-disk image.
        """


GUI_interactions = """
* Right clicking should do ds9-style stretch adjustment. (*not* the same as
  the ``stretch`` property - here I mean "brightness/contrast" adjustment
  within the bounds of a given stretch)
* The user should be able to pan the view interactively.  This can be via
  middle clicking on the new center, click-and-drag, or scrolling (i.e. with
  touchpad a la what ginga does). The properties ``click_drag`` ``click_center``
  and ``scroll`` can turn on/off these options (as does the "selection" mode).
* Zooming - if ``scroll_pan`` is False (probably the default), zooming is via
  the scroll wheel.
* "Selection mode" - see `select_points` method.
* If the user provides an NDData or fits input (assuming the fits file has valid
  WCS), if the cursor is not turned off it shows both the pixel coordinates and
  the WCS coordinates under the cursor.

Initially, *no* keyboard shortcuts should be implemented.  Eventually there
should be a clear mapping from keyboard shortcuts to methods, but until the
methods are stabilized, the keyboard shortcuts should be avoided.
"""

other_requirements = """
* Should be able to hanle ~4k x 4k images without significant performance
  lagging.
* Should be able to handle ~1000x markers without significant performance
  degredation.
* Stretch goal: hould be able to handle ~10k x 10k images acceptable
* Extra-stretchy goal: handle very large datasets using a "tiling" approach.
  This will presumably require different `load_*` functions, and more cleverness
  on the JS side.
"""
