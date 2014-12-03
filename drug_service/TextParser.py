__author__ = 'svema'

import sys
import json
import psycopg2

from drug_entity import *

class TextParser:

    def __init__(self, data):
        self.input_data = data
        print "input_data", data

    def get_drug_data(self):

        summary = "Drug Analysis Report..."

        drug_list = self.input_data.split("\\n")
        print "Drug list", self.input_data.split("\\n")
        print "Drug compound len", str(len(drug_list))

        aDrug = Drug()
        aDrug.Name = drug_list[0]
        summary = "Drug Name: " + aDrug.Name + "\n"

        try:
            con = psycopg2.connect(database='health_care', host='localhost', user='postgres', password='postgres')
            cur = con.cursor()

            query = "SELECT id, drug_name, summary from drug_info where LOWER(drug_name)=LOWER('" + aDrug.Name + "')"
            cur.execute(query)
            rows = cur.fetchall()
            if(len(rows) > 0):
                summary += "Observations: " + str(len(rows)) + " found\n"

                for row in rows:
                    summary += "  >>" + row[2] + "\n"

            i=1
            summary += "\n  Compount wise analysis...\n"
            while i<len(drug_list):
                aCompound = DrugCompound()
                aCompound.Name = drug_list[i]
                query = "SELECT compound, weightage, summary from compound_info where LOWER(compound)=LOWER('" + aCompound.Name + "')"
                print query
                cur.execute(query)
                rows=cur.fetchall()
                summary += "   " + aCompound.Name + ":" + str(len(rows)) + " observation found\n"

                if(len(rows)>0):
                    for row in rows:
                        summary += "     >>" + row[2] + "\n"
                i+=1

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()

        summary += "\n--- End of report ---\n"
        return summary
