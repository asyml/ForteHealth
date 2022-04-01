from cassis import *
import json
import os
import argparse

class forte_medicine_visualization:

    def __init__(self):
        pass
    def typesystem_mapping(self, typesystem, output):
        text_data = output['py/state']['_text']
        annotations = output['py/state']['annotations']
        cas = Cas(typesystem= typesystem)
        cas.sofa_string = text_data
        
        for annotation in annotations:
            tag = annotation['py/object'].split('.')[-1]
            print(tag)
            if tag == 'Token':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.BaseToken')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                lemma = annotation['py/state']['_span']['lemma']
                pos = annotation['py/state']['_span']['pos']
                tid = annotation['py/state']['_span']['_tid']
                cas.add_all([
                Token(begin=begin, end=end, lemmaEntries= lemma, partOfSpeech= pos, tokenNumber= tid )
                ])
            
            if tag =='Subword':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textspan.Segment')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                vocab_id = annotation['py/state']['_span']['vocab_id']
                cas.add_all([
                Token(begin=begin, end=end, id= vocab_id)
                ])

            if tag =='Classification':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.structured.DocumentClassification')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                classification_result = annotation['py/state']['_span']['classification_result']
                cas.add_all([
                Token(begin=begin, end=end, id= vocab_id,label= classification_result )
                ]) 
            
            elif tag == 'Sentence':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textspan.Sentence')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                part_id = annotation['py/state']['_span']['part_id']
                cas.add_all([
                Token(begin=begin, end=end, segmentId = part_id)
                ])

            elif tag == 'Phrase':
                
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                phrase_type = annotation['py/state']['_span']['phrase_type']
                if phrase_type =='NP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.NP')
                elif phrase_type =='ADJP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.ADJP')
                elif phrase_type =='ADVP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.ADVP')
                elif phrase_type =='CONJP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.CONJP')
                elif phrase_type =='INTJ':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.INTJ')
                elif phrase_type =='LST':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.LST')
                elif phrase_type =='PP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.PP')
                elif phrase_type =='PRT':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.PRT')
                elif phrase_type =='SBAR':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.SBAR')
                elif phrase_type =='UCP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.UCP')
                elif phrase_type =='VP':
                    Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.VP')
                cas.add_all([
                Token(begin=begin, end=end, segmentId = part_id)
                ])

            elif tag == 'Sentence':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textspan.Sentence')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                part_id = annotation['py/state']['_span']['part_id']
                cas.add_all([
                Token(begin=begin, end=end, segmentId = part_id)
                ])
            


            elif tag =='EntityMention':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.EntityMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                Token_entity = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.Entity')
                Token_element = typesystem.get_type('org.apache.ct akes.typesystem.type.refsem.Element')
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
            
           

            elif tag == 'ClinicalEntityMention':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.EntityMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                polarity = -1 if annotation['py/state']['polarity']==True else 1
                print(polarity, annotation['py/state']['polarity'], type(annotation['py/state']['polarity']))
                cas.add_all([
                Token(begin= begin, end= end, polarity= polarity)
                ])

            elif tag =='Description':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.Description')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])

            elif tag == 'FrequencyAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationFrequency')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])

            elif tag == 'DurationAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationDuration')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])

            elif tag == 'RouteAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationRoute')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                in_take_method = annotation['py/state']['_span']['in_take_method']
                cas.add_all([
                Token(begin= begin, end= end, value= in_take_method)
                ])

            elif tag == 'SuffixStrengthAnnotation' or 'FractionStrengthAnnotation' or 'RangeStrengthAnnotation' or 'DecimalStrengthAnnotation' or 'StrengthAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationStrength')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end, value= in_take_method)
                ])

            elif tag == 'DrugChangeStatusAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationStatusChange')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                change_status =  annotation['py/state']['_span']['change_status']
                cas.add_all([
                Token(begin= begin, end= end, value= change_status)
                ])

            elif tag == 'DosagesAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationDuration')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])

            elif tag == 'FormAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.refsem.MedicationForm')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])

            elif tag == 'DrugMentionAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.textsem.MedicationMention')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']

                status = annotation['py/state']['_span']['status']
                confidence = annotation['py/state']['_span']['confidence']
                frequency = annotation['py/state']['_span']['frequency']
                duration = annotation['py/state']['_span']['duration']
                route = annotation['py/state']['_span']['route']
                drug_change_status = annotation['py/state']['_span']['drug_change_status']
                dosage = annotation['py/state']['_span']['dosage']
                strength = annotation['py/state']['_span']['strength']
                form = annotation['py/state']['_span']['form']
                start_date = annotation['py/state']['_span']['start_date']
                cas.add_all([
                Token(begin= begin, end= end, medicationFrequency= frequency, medicationDuration= duration, medicationRoute= route,medicationStatusChange= drug_change_status, medicationDosage= dosage, medicationStrength= strength, medicationForm= form, startDate= start_date )
                ])

            elif tag == 'ChunkAnnotation':
                Token = typesystem.get_type('org.apache.ctakes.typesystem.type.syntax.Chunk')
                begin = annotation['py/state']['_span']['begin']
                end = annotation['py/state']['_span']['end']
                cas.add_all([
                Token(begin= begin, end= end)
                ])
        
        return cas

    

if __name__ == "__main__":
    obj = forte_medicine_visualization()
    my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    my_parser.add_argument('typesystem',
                        help='typesystem_path')

    my_parser.add_argument('json',
                        help='json_output_path')

    my_parser.add_argument('output',
                        help='output_xmi_path')

    # Execute parse_args()
    args = my_parser.parse_args()
    print(args)
    with open(args.typesystem, 'rb') as f:
        typesystem = load_typesystem(f)
    with open(args.json, 'rb') as f:
        output = json.load(f)
    cas = obj.typesystem_mapping(typesystem, output)

    cas.to_xmi(args.output)
    os.system("./annotationViewer.sh ")