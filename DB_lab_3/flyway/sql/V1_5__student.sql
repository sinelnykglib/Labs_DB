INSERT INTO Student(Student_ID, BirthDate, Sex, RegTypeName, ClassProfile, ClassLang, ExamYear, Place_ID, School_ID)
SELECT DISTINCT OUTID, Birth, SEXTYPENAME, REGTYPENAME, ClassProfileName, ClassLangName, year,
(SELECT DISTINCT Place.Place_ID
FROM Place
WHERE Place.RegName=zno_data.REGNAME AND Place.AreaName=zno_data.AREANAME AND Place.TerName=zno_data.TERNAME) as pid,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
using(Place_ID)
WHERE School.Name=zno_data.EOName AND School.ParentName=zno_data.EOParent
AND Place.TerName=zno_data.EOTerName AND Place.AreaName=zno_data.EOAreaName ) as school_id
FROM zno_data
WHERE Birth IS NOT NULL
ON CONFLICT DO NOTHING;