#!/usr/bin/env python

from xml.dom import minidom as DOM

class Question:
    """
    A question object is made of a question and an answer
    """
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    
    def __str__(self):
        return "%s -> %s" % (self.question, self.answer)

class QuizzReader:
    qp_stack = []
    sqp_dict = {}
    q_list = []
    
    def parseSQP(self, node):
        sqp_name = node.getAttribute('name')
        parts = []
        for partnode in node.childNodes:
            if partnode.nodeType == DOM.Node.ELEMENT_NODE:
                if partnode.nodeName == 'p':
                    textnode = partnode.childNodes[0] 
                    text = textnode.data
                    parts.append(text.strip())
                    
        self.sqp_dict[sqp_name] = parts
    
    def parseQ(self, node, qp_from_parent=None):    
        qp_from_node = node.getAttribute('qp')
        if qp_from_node:
            self.qp_stack.append(qp_from_node)
        else:
            self.qp_stack.append(qp_from_parent)
    
        sqp = node.getAttribute('sqp_name')
        if sqp:
            sqp_list = self.sqp_dict[sqp]
        else:
            sqp_list = None
        
        q_index = 0
        for child in node.childNodes:
            if child.nodeType == DOM.Node.ELEMENT_NODE:
                if node.nodeName == 'q':
                    if sqp_list:
                        self.parseQ(child, sqp_list[q_index])
                    else:
                        self.parseQ(child)
                    q_index += 1
            elif child.nodeType == DOM.Node.TEXT_NODE:
                text = child.data.strip()
                if text and not text == '#':
                    q_object = Question("/".join(self.qp_stack), text)
                    self.q_list.append(q_object)
        
        self.qp_stack.pop()

    def read(self, xml_file):
        doc = DOM.parse(xml_file)
        root = doc.childNodes[0]
        for node in root.childNodes:
            if node.nodeType == DOM.Node.ELEMENT_NODE:
                if node.nodeName == 'sqp':
                    self.parseSQP(node)
                elif node.nodeName == 'q':
                    self.parseQ(node)


if __name__ == "__main__":
    reader = QuizzReader()
    reader.read("../quizz1.xml")
    
    for q in reader.q_list:
        print q
    