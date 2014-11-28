import psycopg2
import sys
import json


class DrugAnalyzer:

    def __init__(self, json_data):
        self.json_data = json_data
        self.summary = []
        print "Class initialized"

    def check_data(self):
        con = None

        try:
            con = psycopg2.connect(database='health_care', host='localhost', user='postgres', password='postgres')
            cur = con.cursor()
            cur.execute('SELECT version()')
            ver = cur.fetchone()
            print ver

            cur = con.cursor()
            cur.execute('SELECT id, drug_name from drug_info')
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
            'drug': 'unknown',
            'message' : "Drug analysis report goes here",
            'caution' : 'Not available'
        }
        return json.dumps(analysis)