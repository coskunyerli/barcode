import sys


class FontSize:
    @classmethod
    def totalPriceFontSize(cls):
        return cls.__fontSize(42,72,72)

    @classmethod
    def dialogNameLabelFontSize(cls):
        return cls.__fontSize(18,24,24)

    @classmethod
    def totalPriceInPriceDialogFontSize(cls):
        return cls.__fontSize(36,48,48)

    @classmethod
    def __fontSize(cls,wf,mf,of):
        if sys.platform == 'win32' or sys.platform == 'win64':
            fontSize = wf
        elif sys.platform == 'darwin':
            fontSize = mf
        else:
            fontSize = of
        return fontSize