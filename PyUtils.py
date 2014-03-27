#encoding: utf-8
'''
Created on 2013-9-11

@author: zuojingchao01
'''

from Log import Log
import io
import re
import xml.dom.minidom
import xml.sax
import urlparse
class PyUtils():
    log = Log.get_logger("CheckerUtils")

    
    '''parsing xml related'''
    '''
    By monkeypatching the minidom content handler I was able to record line and column number for each node (as the 'parse_position' attribute). 
    copy from stackoverflow
    '''
    #定义sax解析器
    _parser = xml.sax.make_parser()
    #记录解析器原来的setContentHandler
    _orig_set_content_handler = _parser.setContentHandler
    @staticmethod
    def set_content_handler(dom_handler):
        #自定义startElementNS属性
        def startElementNS(name, tagName , attrs):
            orig_start_cb(name, tagName, attrs)
            cur_elem = dom_handler.elementStack[-1]
            cur_elem.parse_position = (CheckerUtils._parser._parser.CurrentLineNumber, CheckerUtils._parser._parser.CurrentColumnNumber)
        #记录dom_handler原来的startElementNS
        orig_start_cb = dom_handler.startElementNS
        #将自定义的startElementNS替换dom_handler的startElementNS
        dom_handler.startElementNS = startElementNS
        #将dom_handler传递给sax解析器的ContentHandler
        CheckerUtils._orig_set_content_handler(dom_handler)
    
    '''
             以utf-8编码读取xml文件并返回dom对象
    '''
    @staticmethod
    def parse_xml(xml_file):
        CheckerUtils._parser.setContentHandler = CheckerUtils.set_content_handler
        dom = xml.dom.minidom.parse(xml_file, CheckerUtils._parser)
        return dom

    '''
    schema 文件属性校验
    '''
    @staticmethod
    def is_xml_encoding_utf8(xml_file):
        #读xml文件的第一行
        line = io.open(xml_file, encoding='utf-8').readline();
        line = line.strip().strip("<").strip(">").strip("?")
        pattern = re.compile(".*encoding\s*=\s*(\S*).*")
        m = re.match(pattern, line)
        if m is not None:
            file_encoding = m.group(1).strip("'").strip("\"").lower()
            if file_encoding == "utf-8":
                return True
            else :
                CheckerUtils.log.error("encoding[%s] is not utf-8", file_encoding)
                return False
        else:
            CheckerUtils.log.error("can not parse encoding from 1st line[%s] in xml[%s]", line, xml_file)
            return False
    '''
    子节点数量
    '''
    @staticmethod
    def children_nodes_number( node):
        i = 0
        for child_node in node.childNodes:
            if child_node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                i = i + 1
        return i


    '''
    查看参与正则运算的parameter中有几个parameter
    '''
    @staticmethod
    def count_groups(parameter):
        pattern = re.compile(parameter)
        return  pattern.groups


    
    ''' python 动态调用相关'''

    @staticmethod
    def import_module(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
    @staticmethod
    def make_str_2_map(string, delimiter, kv_delimiter):
        map_value = {}
        array_value = string.split(delimiter)
        for item in array_value:
            kv_items = item.split(kv_delimiter)
            if len(kv_items) >= 2:
                map_value[kv_items[0]]="=".join(kv_items[1:])
            elif len(kv_items)==1:
                    map_value[kv_items[0]]=""
        return map_value
    
    '''解析url，获取url_params_map'''
    @staticmethod
    def get_url_params_map(url):
        (scheme, hostname, path, url_params, query, fragment) = urlparse.urlparse(url, "", True)
        url_parmas_map = CheckerUtils.make_str_2_map(url_params, "&", "=")
        return url_parmas_map
