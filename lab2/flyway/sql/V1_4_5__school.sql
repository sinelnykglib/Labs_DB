INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT EONAME, EOParent,
(SELECT DISTINCT a.Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE a.RegName=zno_data.REGNAME AND a.AreaName=zno_data.AREANAME AND
a.TerName=zno_data.TERNAME) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT UkrPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=UkrPTRegName AND AreaName=UkrPTAreaName AND
TerName=UkrPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT histPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=histPTRegName AND AreaName=histPTAreaName AND
TerName=histPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT mathPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=mathPTRegName AND AreaName=mathPTAreaName AND
TerName=mathPTTerName) as place_id
FROM zno_data
ON CONFLICT  DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT physPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=physPTRegName AND AreaName=physPTAreaName AND
TerName=physPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT chemPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=chemPTRegName AND AreaName=chemPTAreaName AND
TerName=chemPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT bioPTName, null,
(SELECT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=bioPTRegName AND AreaName=bioPTAreaName AND
TerName=bioPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT geoPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=geoPTRegName AND AreaName=geoPTAreaName AND
TerName=geoPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT engPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL)  as a
WHERE RegName=engPTRegName AND AreaName=engPTAreaName AND
TerName=engPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT fraPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=fraPTRegName AND AreaName=fraPTAreaName AND
TerName=fraPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT deuPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=deuPTRegName AND AreaName=deuPTAreaName AND
TerName=deuPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO School (Name, ParentName, Place_ID)
SELECT DISTINCT spaPTName, null,
(SELECT DISTINCT Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=spaPTRegName AND AreaName=spaPTAreaName AND
TerName=spaPTTerName) as place_id
FROM zno_data
ON CONFLICT DO NOTHING;
