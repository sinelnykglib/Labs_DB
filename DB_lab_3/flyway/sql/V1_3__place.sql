INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT REGNAME, AREANAME, TERNAME
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT EORegName, EOAreaName, EOTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT UkrPTRegName, UkrPTAreaName, UkrPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT histPTRegName, histPTAreaName, histPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT mathPTRegName, mathPTAreaName, mathPTTerNAme
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT physPTRegName, physPTAreaName, physPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT chemPTRegName, chemPTAreaName, chemPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT bioPTRegName, bioPTAreaName, bioPTTerNAme
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT geoPTRegName, geoPTAreaName, geoPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT engPTRegName, engPTAreaName, engPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT fraPTRegName, fraPTAreaName, fraPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT deuPTRegName, deuPTAreaName, deuPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;

INSERT INTO Place(RegName, AreaName, TerName)
SELECT DISTINCT spaPTRegName, spaPTAreaName, spaPTTerName
FROM zno_data
ON CONFLICT DO NOTHING;