import psycopg2
import sys
import json


class DrugAnalyzer:

    def __init__(self, data):
        self.input_data = data
        self.summary = "To be defined"

        print "Class initialized"

    def check_data(self):
        print 'check data invoked'

        drug_list = self.input_data.splitlines()
        print "Drug list", self.input_data.split("\\n")
        print "Drug compound len", str(len(drug_list))

        aDrug_Name = drug_list[0]
        self.summary += "Drug Name: ", aDrug_Name

        con = None

        try:
            con = psycopg2.connect(database='health_care', host='localhost', user='postgres', password='postgres')
            cur = con.cursor()

            query = "SELECT id, drug_name from drug_info where LOWER(drug_name)=LOWER('" + self.json_data['drug'] + "')"
            print query

            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print "Drug: ", row[1]
                subcur = con.cursor()
                subcur.execute("select compound, weightage from compound_info where drug_id='" + row[0] + "'")
                subrows = subcur.fetchall()
                for subrow in subrows:
                    print "    ", subrow[0],"    ", subrow[1]

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()

    def add_summary(self, message):
        self.summary.append(message)
        print "added to summary"

    def output(self):
        print "Output generated"
        analysis = {
            'drug': self.json_data['drug'],
            'message' : "Drug analysis safe for usage",
            'caution' : 'No specific warnings'
        }
        return json.dumps(analysis)