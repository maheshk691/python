import xml.etree.ElementTree as xml

def getMappingsNode(node, nodeName):
    if node.findall('*'):
        for n in node.findall('*'):
            if nodeName in n.tag:
                return n
        else:
            return getMappingsNode(n, nodeName)

def getMappings(rootNode):
    mappingsNode = getMappingsNode(rootNode, 'mappings')
    mapping = {}

    for prop in mappingsNode.findall('*'):
        key = ''
        val = ''

        for child in prop.findall('*'):
            if 'name' in child.tag:
                key = child.text

            if 'value' in child.tag:
                val = child.text

        if val and key:
            mapping[key] = val

    return mapping

pomFile = xml.parse('pom.xml')
root = pomFile.getroot()

mappings = getMappings(root)
print (mappings)