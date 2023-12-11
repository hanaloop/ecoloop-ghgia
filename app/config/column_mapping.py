iorgsite_map = {
    "단지명": "complexName",
    "회사명": "companyName",
    "공장관리번호": "factoryManagementNumber",
    "공장대표주소(도로명)": "streetAddress",
    "공장대표주소(지번)": "landAddress",
    "사업자등록번호": "businessRegistrationNum",
    "대표업종차수": "sectorIds",
    "대표업종번호": "sectorIdMain",
    "업종번호": "sectorIds",
    "업종명": "sectorNames",
    "시도": "addressRegionName",
    "시군구": "addressSubRegion",
    "설립구분": "establishmentType",
    "입주형태": "propertyResidence",
    "보유구분": "propertyOwnership",
    "최초승인일": "approvalDateInitial",
    "승인일": "approvalDate",
    "최초등록일": "registrationDateInitial",
    "등록구분": "registrationType",
    "등록일": "registrationDate",
    "사업유형": "businessType",
    "전화번호": "phoneNumber",
    "남종업원": "numEployeesMale",
    "여종업원": "numEployeesFemale",
    "외국인(남)": "numEployeesForeignMale",
    "외국인(여)": "numEployeesForeignFemale",
    "종업원수": "numEmployeesTotal",
    "생산품": "products",
    "주원자재": "mainRawMaterials",
    "공장크기": "sizeCategory",
    "용도지역": "zoneType",
    "지목": "landType",
    "용지면적": "landArea",
    "제조시설면적": "manufacturingFacilityArea",
    "부대시설면적": "auxiliaryFacilityArea",
    "건축면적": "buildingArea",
    "대기등급": "airQualityGrade",
    "수질등급": "waterQualityGrade",
    "소음/진동여부": "noiseVibrationStatus",
    "생활용수": "livingWaterUsage",
    "산업용수": "industrialWaterUsage",
    "전력": "electricity",
    "석유": "oil",
    "가스": "gas",
    "기타": "others"
}
iorganization_map = {
    "status": "에러 및 정보 코드",
    "modify_date":"dateModified",
    "corp_code": "erefId",
    "corp_name": "legalName",
    "corp_name_eng": "legalNameEng",
    "stock_name": "stockName",
    "stock_code": "tickerSymbol",
    "ceo_nm": "ceoName",
    "corp_cls": "corpClass",
    "jurir_no": "corpRegistNum",
    "bizr_no": "registNumber",
    "adres": "streetAddress",
    "hm_url": "hompage",
    "ir_url": "website",
    "phn_no": "telephone",
    "fax_no": "faxNumber",
    "induty_code": "industryCode",
    "est_dt": "foundingDate"
}

financial_map = {
    "corp_code": "dartId",
    "stock_code": "stockCode",
    "fs_div": "fsDiv",
    "fs_nm": "fsName",
    "sj_div": "sjDiv",
    "sj_nm": "sjNm",
    "account_nm": "accountName",
    "thstrm_nm": "termName",
    "termStart": "termStart",
    "termEnd": "termEnd",
    "thstrm_amount": "amount",
    "thstrm_add_amount": "accumAmount",
    "ord": "ord",
    "currency": "currency",
    "reprt_code": "reportCode"
}

emission_data_cols = [
    "uncertainty", "categoryName", "categoryUid", "countryId", "regionName", 
    "regionUid", "sectorName", "sectorUid", "periodLength", "periodStartDt", 
    "periodEndDt", "pollutantId", "emissionDirect", "emissionElec", "emissionSteam", 
    "emissionOthers", "emissionTotal"
]

ipcc_to_gir_code = {
    '2.A' : 'A.  광물산업', 
    '2.B' : 'B.  화학산업', 
    '2.C' : 'C.  금속산업',
}

code_dict = {
    "07110": "2.A.3",
    "19101": "2.B",
    "20111": "2.B.8",
    "23311": "2.A.1",
    "23312": "2.A.2",
    "23321": "2.A.1",
    "23991": "2.A.5",
    "24111": "2.C.1",
    "24112": "2.C.1",
    "24113": "2.C.2",
    "24119": "2.C.1",
    "24212": "2.C.3",
    "24219": "2.C.4",
    "41221": "2.A.6"
}


address_dict = {
    "강원특별자치도|강릉시": "강원특별자치도|강릉시",
    "강원특별자치도|고성군": "강원특별자치도|고성군",
    "강원특별자치도|동해시": "강원특별자치도|동해시",
    "강원특별자치도|삼척시": "강원특별자치도|삼척시",
    "강원특별자치도|속초시": "강원특별자치도|속초시",
    "강원특별자치도|양구군": "강원특별자치도|양구군",
    "강원특별자치도|양양군": "강원특별자치도|양양군",
    "강원특별자치도|영월군": "강원특별자치도|영월군",
    "강원특별자치도|원주시": "강원특별자치도|원주시",
    "강원특별자치도|인제군": "강원특별자치도|인제군",
    "강원특별자치도|정선군": "강원특별자치도|정선군",
    "강원특별자치도|철원군": "강원특별자치도|철원군",
    "강원특별자치도|춘천시": "강원특별자치도|춘천시",
    "강원특별자치도|태백시": "강원특별자치도|태백시",
    "강원특별자치도|평창군": "강원특별자치도|평창군",
    "강원특별자치도|홍천군": "강원특별자치도|홍천군",
    "강원특별자치도|화천군": "강원특별자치도|화천군",
    "강원특별자치도|횡성군": "강원특별자치도|횡성군",
    "경기|가평군": "경기도|가평군",
    "경기|고양시 일산동구": "경기도|고양시 일산동구",
    "경기|고양시 일산서구": "경기도|고양시 일산서구",
    "경기|광명시": "경기도|광명시",
    "경기|광주시": "경기도|광주시",
    "경기|군포시": "경기도|군포시",
    "경기|김포시": "경기도|김포시",
    "경기|남양주시": "경기도|남양주시",
    "경기|부천시": "경기도|부천시",
    "경기|수원시 권선구": "경기도|수원시 권선구",
    "경기|수원시 영통구": "경기도|수원시 영통구",
    "경기|시흥시": "경기도|시흥시",
    "경기|안산시 단원구": "경기도|안산시 단원구",
    "경기|안성시": "경기도|안성시",
    "경기|안양시 동안구": "경기도|안양시 동안구",
    "경기|안양시 만안구": "경기도|안양시 만안구",
    "경기|양주시": "경기도|양주시",
    "경기|양평군": "경기도|양평군",
    "경기|여주시": "경기도|여주시",
    "경기|연천군": "경기도|연천군",
    "경기|용인시 기흥구": "경기도|용인시 기흥구",
    "경기|용인시 처인구": "경기도|용인시 처인구",
    "경기|의왕시": "경기도|의왕시",
    "경기|의정부시": "경기도|의정부시",
    "경기|이천시": "경기도|이천시",
    "경기|파주시": "경기도|파주시",
    "경기|평택시": "경기도|평택시",
    "경기|포천시": "경기도|포천시",
    "경기|하남시": "경기도|하남시",
    "경기|화성시": "경기도|화성시",
    "경남|거제시": "경상남도|거제시",
    "경남|거창군": "경상남도|거창군",
    "경남|고성군": "경상남도|고성군",
    "경남|김해시": "경상남도|김해시",
    "경남|남해군": "경상남도|남해군",
    "경남|밀양시": "경상남도|밀양시",
    "경남|사천시": "경상남도|사천시",
    "경남|산청군": "경상남도|산청군",
    "경남|양산시": "경상남도|양산시",
    "경남|의령군": "경상남도|의령군",
    "경남|진주시": "경상남도|진주시",
    "경남|창녕군": "경상남도|창녕군",
    "경남|창원시 마산합포구": "경상남도|창원시 마산합포구",
    "경남|창원시 마산회원구": "경상남도|창원시 마산회원구",
    "경남|창원시 성산구": "경상남도|창원시 성산구",
    "경남|창원시 의창구": "경상남도|창원시 의창구",
    "경남|창원시 진해구": "경상남도|창원시 진해구",
    "경남|통영시": "경상남도|통영시",
    "경남|하동군": "경상남도|하동군",
    "경남|함안군": "경상남도|함안군",
    "경남|함양군": "경상남도|함양군",
    "경남|합천군": "경상남도|합천군",
    "경북|경산시": "경상북도|경산시",
    "경북|경주시": "경상북도|경주시",
    "경북|고령군": "경상북도|고령군",
    "경북|구미시": "경상북도|구미시",
    "경북|김천시": "경상북도|김천시",
    "경북|문경시": "경상북도|문경시",
    "경북|봉화군": "경상북도|봉화군",
    "경북|상주시": "경상북도|상주시",
    "경북|성주군": "경상북도|성주군",
    "경북|안동시": "경상북도|안동시",
    "경북|영덕군": "경상북도|영덕군",
    "경북|영양군": "경상북도|영양군",
    "경북|영주시": "경상북도|영주시",
    "경북|영천시": "경상북도|영천시",
    "경북|예천군": "경상북도|예천군",
    "경북|울릉군": "경상북도|울릉군",
    "경북|울진군": "경상북도|울진군",
    "경북|의성군": "경상북도|의성군",
    "경북|청도군": "경상북도|청도군",
    "경북|청송군": "경상북도|청송군",
    "경북|칠곡군": "경상북도|칠곡군",
    "경북|포항시 남구": "경상북도|포항시 남구",
    "경북|포항시 북구": "경상북도|포항시 북구",
    "광주|광산구": "광주광역시|광산구",
    "광주|동구": "광주광역시|동구",
    "대구|군위군": "대구광역시|군위군",
    "대구|남구": "대구광역시|남구",
    "대구|달서구": "대구광역시|달서구",
    "대구|달성군": "대구광역시|달성군",
    "대구|북구": "대구광역시|북구",
    "대구|서구": "대구광역시|서구",
    "대구|수성구": "대구광역시|수성구",
    "대전|대덕구": "대전광역시|대덕구",
    "대전|서구": "대전광역시|서구",
    "대전|유성구": "대전광역시|유성구",
    "대전|중구": "대전광역시|중구",
    "부산|강서구": "부산광역시|강서구",
    "부산|금정구": "부산광역시|금정구",
    "부산|기장군": "부산광역시|기장군",
    "부산|남구": "부산광역시|남구",
    "부산|동구": "부산광역시|동구",
    "부산|동래구": "부산광역시|동래구",
    "부산|부산진구": "부산광역시|부산진구",
    "부산|북구": "부산광역시|북구",
    "부산|사상구": "부산광역시|사상구",
    "부산|사하구": "부산광역시|사하구",
    "부산|서구": "부산광역시|서구",
    "부산|수영구": "부산광역시|수영구",
    "부산|연제구": "부산광역시|연제구",
    "부산|영도구": "부산광역시|영도구",
    "부산|중구": "부산광역시|중구",
    "부산|해운대구": "부산광역시|해운대구",
    "서울|강남구": "서울특별시|강남구",
    "서울|강동구": "서울특별시|강동구",
    "서울|강북구": "서울특별시|강북구",
    "서울|강서구": "서울특별시|강서구",
    "서울|관악구": "서울특별시|관악구",
    "서울|광진구": "서울특별시|광진구",
    "서울|구로구": "서울특별시|구로구",
    "서울|금천구": "서울특별시|금천구",
    "서울|노원구": "서울특별시|노원구",
    "서울|도봉구": "서울특별시|도봉구",
    "서울|동대문구": "서울특별시|동대문구",
    "서울|동작구": "서울특별시|동작구",
    "서울|마포구": "서울특별시|마포구",
    "서울|서대문구": "서울특별시|서대문구",
    "서울|서초구": "서울특별시|서초구",
    "서울|성동구": "서울특별시|성동구",
    "서울|성북구": "서울특별시|성북구",
    "서울|송파구": "서울특별시|송파구",
    "서울|양천구": "서울특별시|양천구",
    "서울|영등포구": "서울특별시|영등포구",
    "서울|용산구": "서울특별시|용산구",
    "서울|은평구": "서울특별시|은평구",
    "서울|종로구": "서울특별시|종로구",
    "서울|중구": "서울특별시|중구",
    "서울|중랑구": "서울특별시|중랑구",
    "세종|세종": "세종특별자치시|세종시",
    "울산|남구": "울산광역시|남구",
    "울산|동구": "울산광역시|동구",
    "울산|북구": "울산광역시|북구",
    "울산|울주군": "울산광역시|울주군",
    "울산|중구": "울산광역시|중구",
    "인천|강화군": "인천광역시|강화군",
    "인천|계양구": "인천광역시|계양구",
    "인천|남동구": "인천광역시|남동구",
    "인천|동구": "인천광역시|동구",
    "인천|미추홀구": "인천광역시|미추홀구",
    "인천|부평구": "인천광역시|부평구",
    "인천|서구": "인천광역시|서구",
    "인천|연수구": "인천광역시|연수구",
    "인천|옹진군": "인천광역시|옹진군",
    "인천|중구": "인천광역시|중구",
    "전남|강진군": "전라남도|강진군",
    "전남|고흥군": "전라남도|고흥군",
    "전남|곡성군": "전라남도|곡성군",
    "전남|광양시": "전라남도|광양시",
    "전남|구례군": "전라남도|구례군",
    "전남|나주시": "전라남도|나주시",
    "전남|담양군": "전라남도|담양군",
    "전남|목포시": "전라남도|목포시",
    "전남|무안군": "전라남도|무안군",
    "전남|보성군": "전라남도|보성군",
    "전남|순천시": "전라남도|순천시",
    "전남|신안군": "전라남도|신안군",
    "전남|여수시": "전라남도|여수시",
    "전남|영광군": "전라남도|영광군",
    "전남|영암군": "전라남도|영암군",
    "전남|완도군": "전라남도|완도군",
    "전남|장성군": "전라남도|장성군",
    "전남|장흥군": "전라남도|장흥군",
    "전남|진도군": "전라남도|진도군",
    "전남|함평군": "전라남도|함평군",
    "전남|해남군": "전라남도|해남군",
    "전남|화순군": "전라남도|화순군",
    "전북|고창군": "전라북도|고창군",
    "전북|군산시": "전라북도|군산시",
    "전북|김제시": "전라북도|김제시",
    "전북|남원시": "전라북도|남원시",
    "전북|무주군": "전라북도|무주군",
    "전북|부안군": "전라북도|부안군",
    "전북|순창군": "전라북도|순창군",
    "전북|완주군": "전라북도|완주군",
    "전북|익산시": "전라북도|익산시",
    "전북|임실군": "전라북도|임실군",
    "전북|장수군": "전라북도|장수군",
    "전북|전주시 덕진구": "전라북도|전주시 덕진구",
    "전북|전주시 완산구": "전라북도|전주시 완산구",
    "전북|정읍시": "전라북도|정읍시",
    "전북|진안군": "전라북도|진안군",
    "제주|서귀포시": "제주특별자치도|서귀포시",
    "제주|제주시": "제주특별자치도|제주시",
    "충남|계룡시": "충청남도|계룡시",
    "충남|공주시": "충청남도|공주시",
    "충남|금산군": "충청남도|금산군",
    "충남|논산시": "충청남도|논산시",
    "충남|당진시": "충청남도|당진시",
    "충남|보령시": "충청남도|보령시",
    "충남|부여군": "충청남도|부여군",
    "충남|서산시": "충청남도|서산시",
    "충남|서천군": "충청남도|서천군",
    "충남|아산시": "충청남도|아산시",
    "충남|연기군": "충청남도|연기군",
    "충남|예산군": "충청남도|예산군",
    "충남|천안시 동남구": "충청남도|천안시 동남구",
    "충남|천안시 서북구": "충청남도|천안시 서북구",
    "충남|청양군": "충청남도|청양군",
    "충남|태안군": "충청남도|태안군",
    "충남|홍성군": "충청남도|홍성군",
    "충북|괴산군": "충청북도|괴산군",
    "충북|단양군": "충청북도|단양군",
    "충북|보은군": "충청북도|보은군",
    "충북|영동군": "충청북도|영동군",
    "충북|옥천군": "충청북도|옥천군",
    "충북|음성군": "충청북도|음성군",
    "충북|제천시": "충청북도|제천시",
    "충북|증평군": "충청북도|증평군",
    "충북|진천군": "충청북도|진천군",
    "충북|청주시 상당구": "충청북도|청주시 상당구",
    "충북|청주시 서원구": "충청북도|청주시 서원구",
    "충북|청주시 청원구": "충청북도|청주시 청원구",
    "충북|청주시 흥덕구": "충청북도|청주시 흥덕구",
    "충북|충주시": "충청북도|충주시"
}


emission_intensity = {
    "2.A":{
        "per_capita": 1.576155271,
        "per_sqrmt": 0.009891076122
    },
    "2.B":{
        "per_capita": 0.04694824017,
        "per_sqrmt": 0.0003317156888
    },
    "2.C":{
        "per_capita": 0.003193994839,
        "per_sqrmt": 0.00001114148534
    }
}
