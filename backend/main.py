import os
import cherrypy_cors
from dotenv import load_dotenv
from jinja2 import Template
import cherrypy
from datetime import datetime
import requests
from formats.ass import AssParser
from translator import translateString
import json
import psycopg2
load_dotenv()

class Stats:
    def __init__(self):
        self.conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )

        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS every_req
                (
                    success int,
                    fail int,
                    error int
                )
                ''')
        self.conn.commit()
        c.execute("SELECT 1 FROM every_req")
        if len(c.fetchall()) == 0:
            c.execute("INSERT INTO every_req VALUES (0, 0, 0)")
            self.conn.commit()


        c.execute('''CREATE TABLE IF NOT EXISTS request_log
                (
                    start_time timestamp,
                    end_time timestamp,
                    content_length int,
                    translate_content_length int,
                    src_lang varchar,
                    tgt_lang varchar,
                    file_format varchar,
                    status varchar
                )
                ''')
        self.conn.commit()
        c.close()

    def track_request(self, status, start_time, end_time,
            content_length,translate_content_length,
            src_lang, tgt_lang, file_format):
        if (status in ["success", "fail", "error"]):
            c = self.conn.cursor()
            c.execute('''UPDATE every_req
                    SET '''+status+''' = '''+status+''' + 1
                   ''')
            self.conn.commit()
            c.execute('''
                    INSERT INTO request_log
                    VALUES(
                        %(start)s,
                        %(end)s,
                        %(content_length)s,
                        %(translate_content_length)s,
                        %(src_lang)s,
                        %(tgt_lang)s,
                        %(file_format)s,
                        %(status)s
                    )
                    ''',
                {
                    "status":status,
                    "start":start_time,
                    "end":end_time,
                    "content_length":content_length,
                    "translate_content_length":translate_content_length,
                    "src_lang":src_lang,
                    "tgt_lang":tgt_lang,
                    "file_format":file_format
                })
            self.conn.commit()
        else:
            raise Exception("Bad status provided")
    def get_request_success_fail_error(self):
        c = self.conn.cursor()
        c.execute("SELECT * from every_req")
        return c.fetchone()
    def get_concurrent_reqs_timeset(self):
        c = self.conn.cursor()
        c.execute("SELECT start_time, end_time from request_log ORDER BY start_time")
        reqs = c.fetchall()


        timestamps = []
        values = []
        #For every logged request
        for i in range(len(reqs)):
            #Calculate how many requests are we translating at a time
            #Iterate over a list containing start time of request and end time of request
            for col_idx, time in enumerate(reqs[i]):
                still_in_time_range = True
                # This is the num of requests we are starting with. We want to start with 0 if we are
                # doing it for the end time, we don't count the current request to the concurrents
                j = 1
                request_num_of_conccurrent = 1 - col_idx
                while still_in_time_range and i-j >= 0:
                    sub_start_time, sub_end_time = reqs[i-j]
                    if sub_start_time < time and time < sub_end_time:
                        request_num_of_conccurrent += 1
                        j += 1
                    else:
                        still_in_time_range = False
                timestamps.append(datetime.timestamp(time))
                values.append(request_num_of_conccurrent)
        return timestamps, values


stats = Stats()

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])
        elif cherrypy.request.method == 'GET':
            return "Hello in subtitle API!"
        else:
            raise cherrypy.HTTPError(400)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def translate_sub(self):
        if cherrypy.request.method == "POST":
            start_time = datetime.now()
            cherrypy.response.headers['Content-Type'] = 'application/json'
            reqBody = cherrypy.request.json
            try:
                src_lang_code = reqBody['src_lang']
                tgt_lang_code = reqBody['tgt_lang']
                file_format = reqBody['format']
                src = reqBody['src']
            except KeyError:
                end_time = datetime.now()
                stats.track_request("fail", start_time, end_time, 0, 0, "", "", "")
                res = { "status":"fail",
                        "data": {
                            "src_lang_code": "",
                            "tgt_lang_code": "",
                            "file_format": "",
                            "src": ""
                        }
                    }
                return json.dumps(res).encode('utf8')
            content_length = len(src)
            if file_format == 'ass' or file_format == 'srt':
                try:
                    parser = AssParser()
                    parsed_strings = parser.parse(src, file_format)
                except Exception as e:
                    end_time = datetime.now()
                    stats.track_request("error", start_time, end_time,
                            content_length, 0, src_lang_code, tgt_lang_code, file_format)
                    cherrypy.log.error("Error parsing ass: "+str(e))
                    res = { "status":"fail",
                            "data": {
                                "src_lang_code": src_lang_code,
                                "tgt_lang_code": tgt_lang_code,
                                "file_format": file_format,
                                "src": "Must be in correct "+file_format+" markup"
                            }
                        }
                    return json.dumps(res).encode('utf-8')
                translate_content_length = len(parsed_strings)
                try:
                    translatedString = translateString(
                            parsed_strings,
                            src_lang_code,
                            tgt_lang_code)
                    result_ass = parser.compose(translatedString, file_format)
                except Exception as e:

                    end_time = datetime.now()
                    stats.track_request("error", start_time, end_time,
                            content_length, translate_content_length,
                            src_lang_code, tgt_lang_code, file_format)

                    cherrypy.log.error(str(e))
                    res = {"status":"error"}
                    return json.dumps(res).encode('utf-8')

                end_time = datetime.now()
                stats.track_request("success", start_time, end_time,
                        content_length, translate_content_length,
                        src_lang_code, tgt_lang_code, file_format)
                res = { "status":"success",
                        "data": {
                            "src_lang_code": src_lang_code,
                            "tgt_lang_code": tgt_lang_code,
                            "file_format": file_format,
                            "src": result_ass
                        }
                    }
                return json.dumps(res).encode('utf-8')
            else:
                end_time = datetime.now()
                stats.track_request("fail", start_time, end_time, 0, 0, src_lang_code, tgt_lang_code,
                        file_format)
                res = { "status":"fail",
                        "data": {
                            "src_lang_code": "",
                            "tgt_lang_code": "",
                            "file_format": "ass|srt",
                            "src": ""
                        }
                    }
                return json.dumps(res).encode('utf-8')
        elif cherrypy.request.method == "OPTIONS":
            cherrypy.response.headers["Access-Control-Allow-Origin"] = '*'
            return "".encode('utf-8')
        else:
            raise cherrypy.HTTPError(status=400)

    @cherrypy.expose
    def stats(self):
        if cherrypy.request.method == "GET":
            success, fail, error = stats.get_request_success_fail_error()

            with open('stats.html', 'r') as f:
                htmlstr = f.read()
            template = Template(htmlstr)
            concurrent_timestamps, concurrent_values = stats.get_concurrent_reqs_timeset()
            rendered = template.render(
                    successes=success,
                    fails=fail,
                    errors=
                    error,
                    concurrent_timestamps=str(concurrent_timestamps),
                    concurrent_values = str(concurrent_values)
                    )
            return rendered
        else:
            raise cherrypy.HTTPError(status=400)
cherrypy_cors.install()
cors_expose = True
try:
    if os.getenv('ALLOW_CORS') == "true":
        cors_expose = True
except Exception:
    pass
print("CORS Bypass: "+str(cors_expose))

cherrypy.config.update({
    'server.socket_host':'0.0.0.0',
    'server.socket_port': 9090,
    'tools.staticdir.on': True,
    'tools.staticdir.dir': os.path.dirname(os.path.realpath(__file__))+'/static/',
    'log.access_file': "access.log",
    'log.error_file': "error.log",
    'cors.expose.on': cors_expose,
    })
cherrypy.quickstart(HelloWorld())
