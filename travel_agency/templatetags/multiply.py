from django import template

register = template.Library()

@register.simple_tag
def multiply(v1, v2):
	return int(v1)*int(v2)