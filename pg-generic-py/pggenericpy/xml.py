import cElementTree as ElementTree

#Code jacked from:
# http://code.activestate.com/recipes/410469-xml-as-dictionary/
class xmlListConfig(list):
	def __init__(self, aList):
		for element in aList:
			if element:
				if len(element) == 1 or element[0].tag != element[1].tag:
					self.append(xmlDictConfig(element))
				elif element[0].tag == element[1].tag:
					self.append(xmlListConfig(element))
			elif element.text:
				text = element.text.strip()
				if text:
					self.append(text)

class xmlDictConfig(dict):
	def __init__(self, parent_element):
		if parent_element.items():
			self.update(dict(parent_element.items()))

		for element in parent_element:
			if element:
				if len(element) == 1 or element[0].tag != element[1].tag:
					aDict = xmlDictConfig(element)
				else:
					aDict = { element[0].tag: xmlListConfig(element) }

				if element.items():
					aDict.update(dict(element.items()))

			elif element.items():
				self.update( { element.tag: dict(element.items()) } )

			else:
				self.update( { element.tag: element.text } )