import yaml
import xml.etree.ElementTree as ET
import sys, os

from abc import abstractmethod, ABC


class XMLGenerator(ABC):
    def __init__(self) -> None:
        self.rootPath = os.path.split(os.path.realpath(__file__))[0]
        self.userCFG = XMLGenerator.yamlParser(self.rootPath + "user_config" + sys.argv[1])

    @abstractmethod
    def plugin(self):
        pass

    @staticmethod
    def yamlParser(path: str) -> dict:
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    @staticmethod
    def indent(elem: ET.Element, level: int = 0) -> None:
        i = '\n' + level * '\t'
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                XMLGenerator.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @staticmethod
    def createElement(name: str, text: str = None, props: dict = {}) -> ET.Element:
        e = ET.Element(name, attrib=props)
        if not text is None:
            e.text = text
        return e
