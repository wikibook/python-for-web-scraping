import time
import sys
import os
import json
import dbm
from urllib.request import urlopen
from urllib.parse import urlencode
from SPARQLWrapper import SPARQLWrapper

def main():
    features = []  # 박물관 정보 저장을 위한 리스트
    for museum in get_museums():
        # 레이블이 있는 경우에는 레이블, 없는 경우에는 s를 추출합니다.
        label = museum.get('label', museum['s'])
        address = museum['address']
        lng, lat = geocode(address)
        
        # 값을 출력해 봅니다.
        print(label, address, lng, lat)
        # 위치 정보를 추출하지 못 했을 경우 리스트에 추가하지 않습니다.
        if lng is None:
            continue
        
        # features에 박물관 정보를 GeoJSON Feature 형식으로 추가합니다.
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lng, lat]},
            'properties': {'label': label, 'address': address},
        })

    # GeoJSON FeatureCollection 형식으로 dict를 생성합니다.
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features,
    }
    # FeatureCollection을 .geojson이라는 확장자의 파일로 저장합니다.
    with open('museums.geojson', 'w') as f:
        json.dump(feature_collection, f)

def get_museums():
    """
    SPARQL을 사용해 DBpedia에서 박물관 정보 추출하기
    """
    print('Executing SPARQL query...', file=sys.stderr)
    
    # SPARQL 엔드 포인트를 지정해서 인스턴스를 생성합니다.
    sparql = SPARQLWrapper('http://ko.dbpedia.org/sparql')
    
    # 한국의 박물관을 추출하는 쿼리입니다.
    sparql.setQuery('''
    SELECT * WHERE {
        ?s rdf:type dbpedia-owl:Museum .
        ?s prop-ko:소재지 ?address .
        OPTIONAL { ?s rdfs:label ?label . }
    } ORDER BY ?s
    ''')

    # 반환 형식을 JSON으로 지정합니다.
    sparql.setReturnFormat('json')

    # query()로 쿼리를 실행한 뒤 convert()로 파싱합니다.
    response = sparql.query().convert()
    print('Got {0} results'.format(len(response['results']['bindings']), file=sys.stderr))
    # 쿼리 결과를 반복 처리합니다.
    for result in response['results']['bindings']:
        # 다루기 쉽게 dict 형태로 변환해서 yield합니다.
        yield {name: binding['value'] for name, binding in result.items()}

# Google Geolocation API
GOOGLE_GEOCODER_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
# DBM(파일을 사용한 Key-Value 데이터베이스)로 지오코딩 결과를 캐시합니다.
# 이 변수는 dict처럼 다룰 수 있습니다.
geocoding_cache = dbm.open('geocoding.db', 'c')

def geocode(address):
    """
    매개변수로 지정한 주소를 지오코딩해서 위도와 경도를 반환합니다.
    """
    if address not in geocoding_cache:
        # 주소가 캐시에 존재하지 않는 경우 지오코딩합니다.
        print('Geocoding {0}...'.format(address), file=sys.stderr)
        time.sleep(1)
        url = GOOGLE_GEOCODER_API_URL + '?' + urlencode({
            'key': os.environ['GOOGLE_API_ID'],
            'language': 'ko',
            'address': address,
        })
        response_text = urlopen(url).read()
        # API 응답을 캐시에 저장합니다.
        # 문자열을 키와 값에 넣으면 자동으로 bytes로 변환합니다.
        geocoding_cache[address] = response_text
    
    # 캐시 내의 API 응답을 dict로 변환합니다.
    # 값은 bytes 자료형이므로 문자열로 변환합니다.
    response = json.loads(geocoding_cache[address].decode('utf-8'))
    try:
        # JSON 형식에서 값을 추출합니다.
        lng = response['results'][0]['geometry']['location']['lng']
        lat = response['results'][0]['geometry']['location']['lat']
        # float 형태로 변환한 뒤 튜플을 반환합니다.
        return (float(lng), float(lat))
    except:
        return (None, None)

if __name__ == '__main__':
    main()