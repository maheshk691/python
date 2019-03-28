import os  
import xml.etree.ElementTree as ET  
import xml.dom.minidom as minidom  
import sys,re  
import argparse  
   
#script updates a pom.xml file with a specific artifactid/groupid/version/type/classifier dependency  
#if the dependency is already there, the version is checked and updated if needed  
#if the dependency is not there, it is added  
#the comparison of dependencies is based on artifactid/groupid/type (and optionally classifier). other fields are ignored  
#the pom file should be in UTF-8  
   
#set the default namespace of the pom.xml file  
pom_ns = dict(pom='http://maven.apache.org/POM/4.0.0')  
ET.register_namespace('',pom_ns.get('pom'))  
   
#parse the arguments  
parser = argparse.ArgumentParser(description='Update pom.xml file with dependency')  
parser.add_argument('pomlocation', help='Location on the filesystem of the pom.xml file to update')  
parser.add_argument('artifactid', help='ArtifactId of the artifact to update')  
parser.add_argument('groupid', help='GroupId of the artifact to update')  
parser.add_argument('version', help='Version of the artifact to update')  
parser.add_argument('type', help='Type of the artifact to update')  
parser.add_argument('--classifier', help='Classifier of the artifact to update',default=None)  
#args = parser.parse_args()  
loc=os.getcwd()   
pomlocation=loc+"\\pom.xml"  
artifactid="jacorb"
groupid="org.jacorb" 
version="2.3.2"
type="type"  
classifier="" 


#pomlocation=args.pomlocation  
#artifactid=args.artifactid  
#groupid=args.groupid  
#version=args.version  
#type=args.type  
#classifier=args.classifier  
   
#read a file and return a ElementTree  
def get_tree_from_xmlfile(filename):  
  if os.path.isfile(filename):  
    tree = ET.parse(filename)  
    return tree  
  else:  
    raise Exception('Error opening '+filename)  
   
#obtain a specific element from an ElementTree based on an xpath  
def get_xpath_element_from_tree(tree,xpath,namespaces):  
  return tree.find(xpath, namespaces)  
   
#returns the content of an element as a string  
def element_to_str(element):  
  return ET.tostring(element, encoding='utf8', method='xml')  
   
#returns an ElementTree as a pretty printed string  
def elementtree_to_str(et):  
  root=et.getroot()  
  ugly_xml = ET.tostring(root, encoding='utf8', method='xml')  
  dom=minidom.parseString(ugly_xml)  
  prettyXML=dom.toprettyxml('\t','\n','utf8')  
  trails=re.compile(r'\s+\n')  
  prettyXML=re.sub(trails,"\n",prettyXML)  
  return prettyXML  
   
#creates an Element object with artifactId, groupId, version, type, classifier elements (used to append a new dependency). classifier is left out if None  
def create_dependency(param_groupid,param_artifactid,param_version,param_type,param_classifier):  
  dependency_element = ET.Element("dependency")  
  groupid_element = ET.Element("groupId")  
  groupid_element.text = param_groupid  
  dependency_element.append(groupid_element)  
  artifactid_element = ET.Element("artifactId")  
  artifactid_element.text = param_artifactid  
  dependency_element.append(artifactid_element)  
  version_element = ET.Element("version")  
  version_element.text = param_version  
  dependency_element.append(version_element)  
  type_element = ET.Element("type")  
  type_element.text = param_type  
  dependency_element.append(type_element)  
  if param_classifier is not None:  
    classifier_element = ET.Element("classifier")  
    classifier_element.text = param_classifier  
    dependency_element.append(classifier_element)  
  return dependency_element  
   
#adds a dependency element to a pom ElementTree. the dependency element can be created with create_dependency   
def add_dependency(pom_et,dependency_element):  
  pom_et.find('pom:dependencies',pom_ns).append(dependency_element)  
  return pom_et  
   
#update the version of a dependency in the pom ElementTree if it is already present. else adds the dependency  
#returns the updated ElementTree and a boolean indicating if the pom ElementTree has been updated  
def merge_dependency(pom_et,param_artifactid,param_groupid,param_type,param_version,param_classifier):  
  artifactfound=False  
  pom_et_changed=False  
  for dependency_element in pom_et.findall('pom:dependencies/pom:dependency',pom_ns):  
    checkgroupid = get_xpath_element_from_tree(dependency_element,'pom:groupId',pom_ns).text  
    checkartifactid = get_xpath_element_from_tree(dependency_element,'pom:artifactId',pom_ns).text  
    checktype = get_xpath_element_from_tree(dependency_element,'pom:type',pom_ns).text  
    if param_classifier is not None:  
      checkclassifier_el = get_xpath_element_from_tree(dependency_element,'pom:classifier',pom_ns)  
      if checkclassifier_el is not None:  
        checkclassifier=checkclassifier_el.text  
      else:  
        checkclassifier=None  
    else:  
      checkclassifier = None  
    if (checkgroupid == param_groupid and checkartifactid == param_artifactid and checktype == param_type and (checkclassifier == param_classifier or param_classifier is None)):  
      artifactfound=True  
      print('Artifact found in '+pomlocation)
      pomversion=dependency_element.find('pom:version',pom_ns).text  
      if pomversion != param_version:  
        print("Artifact has different version in "+pomlocation+". Updating" )
        dependency_element.find('pom:version',pom_ns).text=param_version  
        pom_et_changed=True  
      else:  
        print("Artifact already in "+pomlocation+" with correct version. Update not needed"  )
  if not artifactfound:  
    print ('Artifact not found in pom. Adding' ) 
    dependency_element = create_dependency(param_groupid,param_artifactid,param_version,param_type,param_classifier)  
    pom_et = add_dependency(pom_et,dependency_element)  
    pom_et_changed=True  
  return pom_et,pom_et_changed  
   
#read the file at the pomlocation parameter  
pom_et = get_tree_from_xmlfile(pomlocation)  
   
#merge the dependency into the obtained ElementTree  
pom_et,pom_et_changed=merge_dependency(pom_et,artifactid,groupid,type,version,classifier)  
   
#overwrite the pomlocation if it has been changed   
if pom_et_changed:  
  print ("Overwriting "+pomlocation+" with changes" ) 
  target = open(pomlocation, 'w')  
  target.truncate()  
  target.write(elementtree_to_str(pom_et))  
  target.close()  
else:  
  print (pomlocation+" does not require changes"  )