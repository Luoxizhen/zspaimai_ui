import matplotlib
from matplotlib.font_manager import FontManager
def dd():
    a=matplotlib.get_cachedir()
    print(a)
    b = matplotlib.matplotlib_fname()
    print(b)
    c = matplotlib.get_cachedir()
    print(c)
    fm = FontManager()
    mat_fonts = set(f.name for f in fm.ttflist)
    # print("我{}".format(mat_fonts))
if "__main__" == __name__:
    dd()