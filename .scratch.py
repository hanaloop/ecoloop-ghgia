from datetime import datetime
from types import NoneType
from pyparsing import Union
from prisma import FieldInfo

{"sid":
FieldInfo(annotation=int,
required=True),
"uid":
FieldInfo(annotation=str,
required=True),
"createdByUid":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"dateCreated":
FieldInfo(annotation=datetime,
required=True),
"dateModified":
FieldInfo(annotation=Union[datetime,
NoneType],
required=False),
"dateDeleted":
FieldInfo(annotation=Union[datetime,
NoneType],
required=False),
"deleteFlag":
FieldInfo(annotation=bool,
required=True),
"dateLastAccessed":
FieldInfo(annotation=Union[datetime,
NoneType],
required=False),
"settings":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"additionalProps":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"notes":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"translations":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"accessLevel":
FieldInfo(annotation=Union[int,
NoneType],
required=False),
"status":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"isLocked":
FieldInfo(annotation=bool,
required=True),
"erefId":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"type":
FieldInfo(annotation=str,
required=True),
"id":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"isSubjectRegulation":
FieldInfo(annotation=Union[bool,
NoneType],
required=False),
"applicableRegulations":
FieldInfo(annotation=List[str],
required=True),
"latitude":
FieldInfo(annotation=Union[float,
NoneType],
required=False),
"longitude":
FieldInfo(annotation=Union[float,
NoneType],
required=False),
"addressCountryId":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"addressRegionName":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"addressRegionUid":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"addressRegion":
FieldInfo(annotation=Union[Region,
NoneType],
required=False),
"addressSubRegion":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"addressLocality":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"postalCode":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"streetAddress":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"email":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"faxNumber":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"foundingDate":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"legalName":
FieldInfo(annotation=str,
required=True),
"legalNameEng":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"logoUrl":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"coverImageUrl":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"headline":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"subheadline":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"tagline":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"slogan":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"pageSetup":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"taxID":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"telephone":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"website":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"tickerSymbol":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"brand":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"description":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"summary":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"keywords":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"registNumber":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"identifier":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"name":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"offerings":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"solutions":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"history":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"certifications":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"sectorUid":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"sector":
FieldInfo(annotation=Union[Sector,
NoneType],
required=False),
"specialties":
FieldInfo(annotation=List[str],
required=True),
"legalRepName":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"managerName":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"mainProcessing":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"capital":
FieldInfo(annotation=Union[int,
NoneType],
required=False),
"floorArea":
FieldInfo(annotation=Union[int,
NoneType],
required=False),
"numEmployees":
FieldInfo(annotation=Union[int,
NoneType],
required=False),
"sizeCategory":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"orgBoundary":
FieldInfo(annotation=Union[str,
NoneType],
required=False),
"firstPeriodStartDt":
FieldInfo(annotation=Union[datetime,
NoneType],
required=False),
"lastPeriodEndDt":
FieldInfo(annotation=Union[datetime,
NoneType],
required=False),
"features":
FieldInfo(annotation=Union[Json,
NoneType],
required=False),
"sites":
FieldInfo(annotation=Union[List[IOrgSite],
NoneType],
required=False),
"financials":
FieldInfo(annotation=Union[List[IFinancial],
NoneType],
required=False)}
