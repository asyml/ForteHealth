# Copyright 2022 The Forte Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Visualization Processor
"""
from cassis import *
import json
import os

__all__ = [
    "VisualizationProcessor",
]

class VisualizationProcessor:
    def __init__(self):
        pass
    def typesystem_mapping(self, typesystem, output):
        text_data = output['py/state']['_text']
        annotations = output['py/state']['annotations']
        cas = Cas(typesystem= typesystem)
        cas.sofa_string = text_data
        
        for annotation in annotations:
            tag = annotation['py/object'].split('.')[-1]
            if tag == 'Token':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.BaseToken')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin=begin, end=end)
                ])

            elif tag =='EntityMention':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.EntityMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                Token_entity = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.Entity')
                Token_element = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.Element')
                entity= Token_entity(subject=annotation['py/state']['ner_type'])

                cas.add_all([
                Token(begin= begin, end= end, entity= entity )
                ])

            elif tag =='MedicalEntityMention':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.EntityMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                Token_entity = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.Entity')
                Token_element = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.Element')
                entity= Token_entity(subject=annotation['py/state']['ner_type'])
                tids=[]
                for i in annotation['py/state']['umls_entities']['py/state']['data']:
                    if i:
                        tids.append(i['py/state']['_tid'])
                #tids =[annotation['py/state']['umls_entities']['py/state']['data']['_tid'] for i in annotation['py/state']['umls_entities']['py/state']['data']]
                UMLS = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.UmlsConcept')
                List1 = []
                for i in output['py/state']['generics']:
                    if i['py/state']['_tid'] in tids:
                        tui= i['py/state']['tuis']
                        cui= i['py/state']['cui']
                        name= i['py/state']['name']
                        aliases= i['py/state']['aliases']
                    
                        List1.append(UMLS(tui= tui, cui=cui, name= name, aliases =aliases))
                print(List1)
                FSArray1 = typesystem.get_type('uima.cas.FSArray')

                if len(List1)==0:
                    cas.add_all([
                Token(begin=begin, end=end, entity= entity)
                ])
                else:
                    cas.add_all([
                Token(begin=begin, end=end, entity= entity, umls= List1[0])
                ])
                

            elif tag == 'NegationContext':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.EntityMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                polarity = -1 if annotation['py/state']['polarity']==True else 1
                print(polarity, annotation['py/state']['polarity'], type(annotation['py/state']['polarity']))
                cas.add_all([
                Token(begin= begin, end= end, polarity= polarity)
                ])
            
            elif tag == 'Sentence':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textspan.Sentence')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin=begin, end=end)
                ])
        
        return cas

    def run(typesystem_loc: str, json_op_path: str, xmi_op_path: str):
        typesystem_path=typesystem_loc#"./TypeSystem.xml"
        json_output_path=json_op_path#'notes_small_output.json'
        output_xmi_path=xmi_op_path#"./Output/my_cas.xmi"
        obj = VisualizationProcessor()
        
        with open(typesystem_path, 'rb') as f:
            typesystem = load_typesystem(f)
        with open(json_output_path, 'rb') as f:
            output = json.load(f)
        cas = obj.typesystem_mapping(typesystem, output)

        cas.to_xmi(output_xmi_path)
        os.system("./annotationViewer.sh ")