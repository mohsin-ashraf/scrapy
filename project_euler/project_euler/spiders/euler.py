# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import psycopg2
import glob

try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=project_euler user=db_user password=user_pass")
except psycopg2.Error as err:
    print ("Error: Couldn;t connect to the database")
    print (err)

conn.set_session(autocommit=True)

class EulerSpider(scrapy.Spider):
    name = 'euler'
    allowed_domains = ['projecteuler.net']
    start_urls = ['https://projecteuler.net/archives']

    def parse(self, response):
        problem_ids = response.xpath('//td[@class="id_column"]/text()').extract()  
        problem_titles = response.xpath('//a[contains(@href,"problem=")]/text()').extract()
        solved_by = response.xpath('//table[@id="problems_table"]//tr//td[3]//text()').extract()
        


        for index,problem_id in enumerate(problem_ids):
          #  problem_url = "https://projecteuler.net/problem="+problem_id
          #  problem_content = Request(url=problem_url,callback=self.parse_problem)
            
            yield{
                "Problem ID ":problem_id,
                "Problem Title ":problem_titles[index],
                "Problem Solved by ":solved_by[index],
           #     "Problem Description ":problem_content
            }

            

#    def parse_problem(self,response):
#        problem_content = response.xpath('//div[@class="problem_content"]/p/text()').extract()
#        yield problem_content


    def close(self,reason):
        csv_file = max(glob.iglob('*.csv'),key=os.path.getctime)
        csv_data = csv.reader(file(csv_file))
        
        try:
            cur.execute('CREATE TABLE IF NOT EXISTS problem(id varchar,title varchar, solved_by varchar );')
        except psycopg2.Error as err:
            print ("Error: Issue creating the table")
            print (err)

        row_count = 0
        for row in csv_data:
            if row_count != 0:
                conn.execute("INSERT INTO problem (id,title,solved_by) VALUES (%s, %s, %s)",row)
            row_count += 1
        
        conn.close()

