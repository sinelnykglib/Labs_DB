INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 1, OUTID, UkrTestStatus, UkrBall100, UkrBall12, UkrBall, UkrAdaptScale, null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.UkrPTName AND Place.TerName=zno_data.UkrPTTerName AND Place.RegName=zno_data.UkrPTRegName AND Place.AreaName=zno_data.UkrPTAreaName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 2, OUTID, histTestStatus, histBall100, histBall12, histBall,null , null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.histPTName AND Place.TerName=zno_data.histPTName AND Place.AreaName=zno_data.histPTAreaName AND Place.RegName=zno_data.histPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 3, OUTID, mathTestStatus, mathBall100, mathBall12, mathBall, null, null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.mathPTName AND Place.TerName=zno_data.mathPTName AND Place.AreaName=zno_data.mathPTAreaName AND Place.RegName=zno_data.mathPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 4, OUTID, physTestStatus, physBall100, physBall12, physBall,null , null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.physPTName AND Place.TerName=zno_data.physPTName AND Place.AreaName=zno_data.physPTAreaName AND Place.RegName=zno_data.physPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 5, OUTID, chemTestStatus, chemBall100, chemBall12, chemBall,null , null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.chemPTName AND Place.TerName=zno_data.chemPTName AND Place.AreaName=zno_data.chemPTAreaName AND Place.RegName=zno_data.chemPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 6, OUTID, bioTestStatus, bioBall100, bioBall12, bioBall, null , null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.bioPTName AND Place.TerName=zno_data.bioPTName AND Place.AreaName=zno_data.bioPTAreaName AND Place.RegName=zno_data.bioPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 7, OUTID, geoTestStatus, geoBall100, geoBall12, geoBall,null , null,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.geoPTName AND Place.TerName=zno_data.geoPTName AND Place.AreaName=zno_data.geoPTAreaName AND Place.RegName=zno_data.geoPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 8, OUTID, engTestStatus, engBall100, engBall12, engBall,null , engDPALevel,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.engPTName AND Place.TerName=zno_data.engPTName AND Place.AreaName=zno_data.engPTAreaName AND Place.RegName=zno_data.engPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 9, OUTID, fraTestStatus, fraBall100, fraBall12, fraBall,null , fraDPALevel,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.fraPTName AND Place.TerName=zno_data.fraPTName AND Place.AreaName=zno_data.fraPTAreaName AND Place.RegName=zno_data.fraPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 10, OUTID, deuTestStatus, deuBall100, deuBall12, deuBall,null , deuDPALevel,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.deuPTName AND Place.TerName=zno_data.deuPTName AND Place.AreaName=zno_data.deuPTAreaName AND Place.RegName=zno_data.deuPTRegName
AND School.ParentName IS NULL)
FROM zno_data;

INSERT INTO Test (Subject_ID, Student_ID, TestStatus, Ball100, Ball12, Ball,
 UkrAdaptScale, DPALevel, School_ID)
SELECT 11, OUTID, spaTestStatus, spaBall100, spaBall12, spaBall,null , spaDPALevel,
(SELECT DISTINCT School_ID
FROM School
LEFT JOIN Place
USING (Place_ID)
WHERE School.Name=zno_data.spaPTName AND Place.TerName=zno_data.spaPTName AND Place.AreaName=zno_data.spaPTAreaName AND Place.RegName=zno_data.spaPTRegName
AND School.ParentName IS NULL)
FROM zno_data;
