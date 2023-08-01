from django import template


register = template.Library()


SYMBOLS = {
   'rediska': '*',

}


@register.filter()
def censor(news, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = SYMBOLS[code]

   return f'{news} {postfix}'