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

class Quizz:
    """
    A quizz
    """
    def __init__(self):
        self.questions_list = []
        self.name = "Quizz Name"
    
class QuizzReader:
    qp_stack = []
    sqp_dict = {}
    quizzes_list = []
    
    def read(self, xml_file):
        """
        Reads a file of quizzes
        """
        doc = DOM.parse(xml_file)
        root = doc.childNodes[0]
        self.parse_root(root)

    def parse_root(self, root):
        """
        Parses the root node
        
        The root node contains sqp () and quizz nodes
        """
        for node in root.childNodes:
            if node.nodeType == DOM.Node.ELEMENT_NODE:
                if node.nodeName == 'sqp':
                    self.parse_sqp(node)
                elif node.nodeName == 'quizz':
                    self.current_quizz = Quizz()
                    self.quizzes_list.append(self.current_quizz)
                    self.parse_quizz(node)

    def parse_quizz(self, quizz_node):
        """
        Parses a quizz node
        """
        self.current_quizz.name = quizz_node.getAttribute('name')
        for node in quizz_node.childNodes:
            if node.nodeType == DOM.Node.ELEMENT_NODE:
                if node.nodeName == 'q':
                    self.parse_question(node)
    
    def parse_sqp(self, node):
        sqp_name = node.getAttribute('name')
        parts = []
        for partnode in node.childNodes:
            if partnode.nodeType == DOM.Node.ELEMENT_NODE:
                if partnode.nodeName == 'p':
                    textnode = partnode.childNodes[0] 
                    text = textnode.data
                    parts.append(text.strip())
                    
        self.sqp_dict[sqp_name] = parts
    
    def parse_question(self, node, qp_from_parent=None):
        include = node.getAttribute('include')
        if include and include.lower() == 'false':
            return
        
        qp_from_node = node.getAttribute('qp')
        stacked = True
        if qp_from_node:
            self.qp_stack.append(qp_from_node)
        elif qp_from_parent:
            self.qp_stack.append(qp_from_parent)
        else:
            stacked = False
    
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
                        self.parse_question(child, sqp_list[q_index])
                    else:
                        self.parse_question(child)
                    q_index += 1
            elif child.nodeType == DOM.Node.TEXT_NODE:
                text = child.data.strip()
                if text and not text[0] == '#':
                    q_object = Question(" / ".join(self.qp_stack), text)
                    self.current_quizz.questions_list.append(q_object)
        
        if stacked:
            self.qp_stack.pop()


if __name__ == "__main__":
    reader = QuizzReader()
    reader.read("../data/quizz_v2.xml")
    
    for quizz in reader.quizzes_list:
        print "Quizz: %s" % quizz.name
        for question in quizz.questions_list:
            print question
    