

from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    """ 重写RadioSelect类，使用自定义的模板 """
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'
