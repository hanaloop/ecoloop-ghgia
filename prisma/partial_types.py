from prisma.models import IOrgSite


IOrgSite.create_partial(exclude=["sid"            
,"uid"            
,"createdByUid"   
,"dateCreated"    
,"dateModified"   
,"dateDeleted"    
,"deleteFlag"      
,"settings"       
,"additionalProps"
,"notes",
"keyHash"          ], name= "PostIorgSiteObject", exclude_relational_fields=True)
