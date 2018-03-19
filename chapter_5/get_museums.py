# pip install SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper  

# SPARQL 엔드 포인트를 지정해서 인스턴스를 생성합니다.
sparql = SPARQLWrapper('http://ko.dbpedia.org/sparql')

# 한국의 박물관을 추출하는 쿼리입니다.
sparql.setQuery('''
SELECT * WHERE {
    ?s rdf:type dbpedia-owl:Museum .
    ?s prop-ko:소재지 ?address .
} ORDER BY ?s
''')

# 반환 형식을 JSON으로 지정합니다.
sparql.setReturnFormat('json')

# query()로 쿼리를 실행한 뒤 convert()로 파싱합니다.
response = sparql.query().convert()
for result in response['results']['bindings']:
    # 출력합니다.
    print(result['s']['value'], result['address']['value'])