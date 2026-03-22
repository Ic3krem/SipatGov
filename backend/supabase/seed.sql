-- ============================================================================
-- SipatGov - Seed Data
-- Real Philippine geographic data for map markers
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. REGIONS (17 Philippine regions with PSGC codes)
-- ============================================================================
INSERT INTO regions (id, psgc_code, name, region_code) VALUES
    (1,  '130000000', 'National Capital Region (NCR)',                             'NCR'),
    (2,  '140000000', 'Cordillera Administrative Region (CAR)',                    'CAR'),
    (3,  '010000000', 'Region I - Ilocos Region',                                 'I'),
    (4,  '020000000', 'Region II - Cagayan Valley',                               'II'),
    (5,  '030000000', 'Region III - Central Luzon',                               'III'),
    (6,  '040000000', 'Region IV-A - CALABARZON',                                 'IV-A'),
    (7,  '170000000', 'Region IV-B - MIMAROPA',                                   'IV-B'),
    (8,  '050000000', 'Region V - Bicol Region',                                  'V'),
    (9,  '060000000', 'Region VI - Western Visayas',                              'VI'),
    (10, '070000000', 'Region VII - Central Visayas',                              'VII'),
    (11, '080000000', 'Region VIII - Eastern Visayas',                             'VIII'),
    (12, '090000000', 'Region IX - Zamboanga Peninsula',                           'IX'),
    (13, '100000000', 'Region X - Northern Mindanao',                              'X'),
    (14, '110000000', 'Region XI - Davao Region',                                  'XI'),
    (15, '120000000', 'Region XII - SOCCSKSARGEN',                                 'XII'),
    (16, '160000000', 'Region XIII - Caraga',                                      'XIII'),
    (17, '190000000', 'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)',   'BARMM');

SELECT setval('regions_id_seq', 17);

-- ============================================================================
-- 2. PROVINCES (selected provinces for seed LGUs)
-- ============================================================================
INSERT INTO provinces (id, psgc_code, name, region_id) VALUES
    (1,  '133900000', 'Metro Manila',          1),   -- NCR (special case)
    (2,  '141100000', 'Benguet',               2),   -- CAR
    (3,  '012800000', 'La Union',              3),   -- Region I
    (4,  '034900000', 'Pampanga',              5),   -- Region III
    (5,  '041000000', 'Batangas',              6),   -- Region IV-A
    (6,  '043400000', 'Rizal',                 6),   -- Region IV-A
    (7,  '174000000', 'Palawan',               7),   -- IV-B
    (8,  '050500000', 'Albay',                 8),   -- Region V
    (9,  '063000000', 'Iloilo',                9),   -- Region VI
    (10, '072200000', 'Cebu',                  10),  -- Region VII
    (11, '083700000', 'Leyte',                 11),  -- Region VIII
    (12, '097300000', 'Zamboanga del Sur',      12),  -- Region IX
    (13, '101300000', 'Misamis Oriental',       13),  -- Region X
    (14, '112400000', 'Davao del Sur',          14),  -- Region XI
    (15, '124700000', 'South Cotabato',         15),  -- Region XII
    (16, '166700000', 'Agusan del Norte',       16),  -- Region XIII
    (17, '153600000', 'Lanao del Sur',          17);  -- BARMM

SELECT setval('provinces_id_seq', 17);

-- ============================================================================
-- 3. LGUs (30 real Philippine LGUs with actual coordinates)
-- ============================================================================
INSERT INTO lgus (id, psgc_code, name, lgu_type, province_id, region_id, latitude, longitude, population, income_class, transparency_score) VALUES
    -- NCR cities
    (1,  '133900000', 'City of Manila',              'city', 1,  1,  14.5995124, 120.9842195, 1846513,  '1st', 72.50),
    (2,  '137404000', 'Quezon City',                 'city', 1,  1,  14.6760413, 121.0437003, 2960048,  '1st', 68.30),
    (3,  '137601000', 'City of Makati',              'city', 1,  1,  14.5547400, 121.0244452, 629616,   '1st', 85.10),
    (4,  '137501000', 'City of Pasig',               'city', 1,  1,  14.5764000, 121.0851000, 803159,   '1st', 70.00),
    (5,  '137402000', 'City of Taguig',              'city', 1,  1,  14.5176000, 121.0509000, 886722,   '1st', 75.20),
    (6,  '137403000', 'City of Paranaque',           'city', 1,  1,  14.4793000, 121.0198000, 689992,   '1st', 64.80),
    (7,  '137405000', 'City of Pasay',               'city', 1,  1,  14.5378000, 121.0014000, 416522,   '1st', 58.50),
    (8,  '133901000', 'City of Caloocan',            'city', 1,  1,  14.6488000, 120.9668000, 1661584,  '1st', 55.00),

    -- Luzon (outside NCR)
    (9,  '141102000', 'City of Baguio',              'city', 2,  2,  16.4023000, 120.5960000, 366358,   '1st', 78.60),
    (10, '012801000', 'City of San Fernando (LU)',    'city', 3,  3,  16.6159000, 120.3209000, 132462,   'component', 62.10),
    (11, '034907000', 'City of San Fernando (Pamp)',  'city', 4,  5,  14.6942000, 120.6917000, 306659,   '1st', 66.40),
    (12, '034902000', 'City of Angeles',             'city', 4,  5,  15.1450000, 120.5887000, 462831,   '1st', 60.00),
    (13, '041005000', 'City of Batangas',            'city', 5,  6,  13.7565000, 121.0583000, 351437,   '1st', 61.30),
    (14, '043401000', 'City of Antipolo',            'city', 6,  6,  14.5860000, 121.1761000, 887399,   '1st', 57.80),

    -- Visayas
    (15, '072217000', 'City of Cebu',                'city', 10, 10, 10.3157000, 123.8854000, 964169,   '1st', 80.20),
    (16, '072227000', 'City of Mandaue',             'city', 10, 10, 10.3236000, 123.9223000, 364116,   '1st', 67.50),
    (17, '072234000', 'City of Lapu-Lapu',           'city', 10, 10, 10.3103000, 123.9494000, 497604,   '1st', 63.90),
    (18, '063049000', 'City of Iloilo',              'city', 9,  9,  10.6969000, 122.5644000, 457626,   '1st', 74.40),
    (19, '083747000', 'City of Tacloban',            'city', 11, 11, 11.2543000, 124.9607000, 251881,   '1st', 59.20),

    -- Mindanao
    (20, '112402000', 'City of Davao',               'city', 14, 14,  7.0644000, 125.6077000, 1776949,  '1st', 82.40),
    (21, '097332000', 'City of Zamboanga',           'city', 12, 12,  6.9214000, 122.0790000, 977234,   '1st', 56.70),
    (22, '101318000', 'City of Cagayan de Oro',      'city', 13, 13,  8.4542000, 124.6319000, 728402,   '1st', 71.30),
    (23, '124504000', 'City of General Santos',      'city', 15, 15,  6.1164000, 125.1716000, 697315,   '1st', 65.40),
    (24, '166704000', 'City of Butuan',              'city', 16, 16,  8.9475000, 125.5406000, 372910,   '1st', 60.80),
    (25, '153602000', 'Marawi City',                 'city', 17, 17,  7.9986000, 124.2928000, 201785,   '3rd', 42.10),

    -- Additional municipalities for variety
    (26, '174003000', 'Municipality of Puerto Princesa', 'city', 7,  7,  9.7407000, 118.7353000, 307079, '1st', 69.50),
    (27, '050506000', 'City of Legazpi',             'city', 8,  8,  13.1391000, 123.7438000, 210106,   '1st', 63.20),
    (28, '020401000', 'City of Tuguegarao',          'city', NULL, 4, 17.6131000, 121.7269000, 166334,   '1st', 58.90),
    (29, '150700000', 'City of Cotabato',            'city', NULL, 17, 7.2236000, 124.2464000, 325079,  '1st', 48.30),
    (30, '043403000', 'City of Marikina',            'city', 1,  1,  14.6507000, 121.1029000, 456059,   '1st', 81.70);

SELECT setval('lgus_id_seq', 30);

-- ============================================================================
-- 4. OFFICIALS (5 sample officials)
-- ============================================================================
INSERT INTO officials (id, lgu_id, full_name, position, party, term_start, term_end, is_current) VALUES
    (1, 1,  'Maria Santos',        'City Mayor',        'PDP-Laban',      '2022-06-30', '2025-06-30', true),
    (2, 2,  'Jose Reyes Jr.',      'City Mayor',        'Nacionalista',    '2022-06-30', '2025-06-30', true),
    (3, 15, 'Michael Rama',        'City Mayor',        'BOPK',            '2022-06-30', '2025-06-30', true),
    (4, 20, 'Sebastian Duterte',   'City Mayor',        'HNP',             '2022-06-30', '2025-06-30', true),
    (5, 3,  'Abigail Binay',       'City Mayor',        'UNA',             '2022-06-30', '2025-06-30', true);

SELECT setval('officials_id_seq', 5);

-- ============================================================================
-- 5. DOCUMENTS (sample source documents)
-- ============================================================================
INSERT INTO documents (id, source_portal, source_url, title, document_type, lgu_id, processing_status) VALUES
    (1,  'philgeps', 'https://philgeps.gov.ph/doc/001', 'Manila Annual Budget FY2024',              'budget',       1,  'completed'),
    (2,  'philgeps', 'https://philgeps.gov.ph/doc/002', 'QC Infrastructure Procurement Plan 2024',  'procurement',  2,  'completed'),
    (3,  'dbm',      'https://dbm.gov.ph/doc/003',      'Cebu City LDRRM Fund Allocation',          'budget',       15, 'completed'),
    (4,  'coa',      'https://coa.gov.ph/doc/004',      'Davao City Audit Report 2023',             'audit',        20, 'completed'),
    (5,  'manual',   'https://manila.gov.ph/press/005',  'Manila Mayor Press Release - Hospital',    'press_release', 1, 'completed'),
    (6,  'efoi',     'https://efoi.gov.ph/doc/006',      'Makati City Development Plan 2024-2025',  'plan',         3,  'completed'),
    (7,  'philgeps', 'https://philgeps.gov.ph/doc/007',  'QC Road Rehabilitation Bid Notice',       'bid_notice',   2,  'completed'),
    (8,  'philgeps', 'https://philgeps.gov.ph/doc/008',  'Cebu City School Construction Bid',       'bid_notice',   15, 'completed'),
    (9,  'manual',   'https://davaocity.gov.ph/doc/009', 'Davao City Clean Water Initiative Docs',  'project_doc',  20, 'completed'),
    (10, 'dbm',      'https://dbm.gov.ph/doc/010',      'Makati City Annual Budget FY2025',         'budget',       3,  'completed');

SELECT setval('documents_id_seq', 10);

-- ============================================================================
-- 6. PROMISES (22 promises with varied statuses)
-- ============================================================================
INSERT INTO promises (id, official_id, lgu_id, title, description, category, status, evidence_summary, date_promised, deadline, verified_at, verified_by, confidence_score, source_document_id) VALUES
    -- Manila (Mayor Maria Santos) - 5 promises
    (1,  1, 1,
        'Build 5 new public hospitals',
        'Construction of five new public hospitals across Manila districts to improve healthcare access for residents.',
        'Health', 'in_progress',
        'Two hospitals completed, third under construction as of Q1 2025.',
        '2022-07-15', '2025-12-31', '2025-01-15 10:00:00+08', 'SipatGov Team', 0.80, 5),

    (2,  1, 1,
        'Rehabilitate all Manila public schools',
        'Complete renovation and rehabilitation of all 285 public school buildings in the City of Manila.',
        'Education', 'partially_kept',
        '180 out of 285 schools have been renovated. Budget exhausted for remaining schools.',
        '2022-08-01', '2025-06-30', '2025-02-10 14:00:00+08', 'SipatGov Team', 0.75, 1),

    (3,  1, 1,
        'Zero informal settler families by 2025',
        'Provide permanent housing solutions for all informal settler families within the city.',
        'Housing', 'broken',
        'Only 15% of informal settlers have been relocated. Program significantly behind schedule.',
        '2022-07-15', '2025-06-30', '2025-03-01 09:00:00+08', 'SipatGov Team', 0.90, NULL),

    (4,  1, 1,
        'Free Wi-Fi in all public spaces',
        'Install free high-speed Wi-Fi in all 896 barangays and public parks.',
        'Technology', 'kept',
        'Free Wi-Fi coverage verified in 850+ barangays and all major public parks.',
        '2022-09-01', '2024-12-31', '2025-01-20 11:00:00+08', 'SipatGov Team', 0.85, NULL),

    (5,  1, 1,
        'Increase garbage collection to twice daily',
        'Double garbage collection frequency in all districts from once to twice daily.',
        'Environment', 'kept',
        'Verified through multiple community reports and LGU operational data.',
        '2022-07-20', '2023-06-30', '2023-08-15 10:00:00+08', 'SipatGov Team', 0.92, NULL),

    -- Quezon City (Mayor Jose Reyes Jr.) - 5 promises
    (6,  2, 2,
        'Build 10km protected bike lanes',
        'Construct 10 kilometers of protected bicycle lanes along major QC thoroughfares.',
        'Infrastructure', 'kept',
        '12km of bike lanes completed including segments on Commonwealth and Visayas Ave.',
        '2022-08-15', '2024-12-31', '2024-11-20 15:00:00+08', 'SipatGov Team', 0.95, 2),

    (7,  2, 2,
        'Plant 100,000 trees in QC',
        'Urban greening program targeting 100,000 new trees across Quezon City parks and sidewalks.',
        'Environment', 'in_progress',
        '67,000 trees planted as of March 2025. Program ongoing.',
        '2022-09-01', '2025-12-31', NULL, NULL, NULL, NULL),

    (8,  2, 2,
        'Free college education for QC residents',
        'Expand QC scholarship program to cover full tuition for all qualified QC residents.',
        'Education', 'kept',
        'QC University expansion completed. 15,000+ scholars enrolled in AY 2024-2025.',
        '2022-07-15', '2024-06-30', '2024-08-10 14:00:00+08', 'SipatGov Team', 0.88, NULL),

    (9,  2, 2,
        'Modernize 50 public markets',
        'Full renovation and modernization of 50 public markets across QC.',
        'Infrastructure', 'partially_kept',
        '28 markets renovated. Remaining markets delayed due to vendor relocation issues.',
        '2022-08-01', '2025-06-30', '2025-02-28 09:00:00+08', 'SipatGov Team', 0.70, NULL),

    (10, 2, 2,
        'Deploy 1,000 CCTV cameras citywide',
        'Installation of CCTV security cameras in crime-prone areas and major intersections.',
        'Public Safety', 'pending',
        NULL,
        '2023-01-15', '2025-12-31', NULL, NULL, NULL, NULL),

    -- Cebu City (Mayor Michael Rama) - 4 promises
    (11, 3, 15,
        'Complete SRP development Phase 2',
        'Finish Phase 2 of South Road Properties reclamation and commercial development.',
        'Infrastructure', 'in_progress',
        'Land reclamation 80% complete. Commercial lot bidding has started.',
        '2022-07-01', '2026-06-30', NULL, NULL, NULL, 3),

    (12, 3, 15,
        'Build Cebu City medical center',
        'Construct a world-class 500-bed medical center for Cebuanos.',
        'Health', 'pending',
        NULL,
        '2022-10-01', '2026-12-31', NULL, NULL, NULL, NULL),

    (13, 3, 15,
        'Flood control master plan implementation',
        'Implement comprehensive flood control solutions in 15 flood-prone barangays.',
        'Infrastructure', 'partially_kept',
        '9 out of 15 barangays have completed flood control infrastructure.',
        '2022-08-15', '2025-06-30', '2025-03-10 11:00:00+08', 'SipatGov Team', 0.65, NULL),

    (14, 3, 15,
        'Free shuttle service for students',
        'Provide free shuttle buses for public school students during school months.',
        'Education', 'kept',
        '50 shuttle buses deployed serving 12,000 students daily across 8 routes.',
        '2023-01-01', '2023-06-30', '2023-09-15 10:00:00+08', 'SipatGov Team', 0.91, NULL),

    -- Davao City (Mayor Sebastian Duterte) - 4 promises
    (15, 4, 20,
        'Clean water for all Davao barangays',
        'Ensure 24/7 clean water supply to all 182 barangays including upland communities.',
        'Infrastructure', 'in_progress',
        'Water infrastructure extended to 140 barangays. Upland areas remain challenging.',
        '2022-07-15', '2025-12-31', NULL, NULL, NULL, 9),

    (16, 4, 20,
        'Expand Davao public transport modernization',
        'Replace all traditional jeepneys with modern PUVs and establish 5 new bus routes.',
        'Transportation', 'pending',
        NULL,
        '2023-03-01', '2026-06-30', NULL, NULL, NULL, NULL),

    (17, 4, 20,
        'Build 3 new sports complexes',
        'Construct modern sports complexes in Toril, Buhangin, and Bunawan districts.',
        'Recreation', 'broken',
        'Only one complex (Buhangin) completed. Toril and Bunawan cancelled due to budget reallocation.',
        '2022-08-01', '2024-12-31', '2025-01-30 10:00:00+08', 'SipatGov Team', 0.85, 4),

    (18, 4, 20,
        'Reduce crime rate by 30%',
        'Implement enhanced peacekeeping programs and CCTV systems to reduce overall crime rate.',
        'Public Safety', 'kept',
        'PNP data shows 35% reduction in index crimes from 2022 baseline.',
        '2022-07-15', '2024-12-31', '2025-02-15 14:00:00+08', 'SipatGov Team', 0.78, NULL),

    -- Makati (Mayor Abigail Binay) - 4 promises
    (19, 5, 3,
        'Expand Yellow Card healthcare program',
        'Extend free healthcare benefits to all Makati residents including dental and mental health.',
        'Health', 'kept',
        'Yellow Card program expanded to cover dental, optometry, and mental health services.',
        '2022-07-15', '2024-06-30', '2024-07-20 09:00:00+08', 'SipatGov Team', 0.93, 6),

    (20, 5, 3,
        'Build affordable housing in Makati',
        'Construct 2,000 units of affordable housing for Makati informal settlers.',
        'Housing', 'in_progress',
        '800 units completed in two sites. Third site under construction.',
        '2022-08-01', '2025-12-31', NULL, NULL, NULL, NULL),

    (21, 5, 3,
        'Digital governance portal',
        'Launch comprehensive online portal for all government transactions and permit processing.',
        'Technology', 'kept',
        'Portal launched with 95% of transactions available online. Processing time reduced by 60%.',
        '2022-09-01', '2024-03-31', '2024-04-15 11:00:00+08', 'SipatGov Team', 0.88, 10),

    (22, 5, 3,
        'Zero open drainage by 2025',
        'Cover and rehabilitate all open drainage systems in Makati.',
        'Infrastructure', 'pending',
        NULL,
        '2023-01-01', '2025-12-31', NULL, NULL, NULL, NULL);

SELECT setval('promises_id_seq', 22);

-- ============================================================================
-- 7. PROJECTS (15 projects with PhilGEPS-style references)
-- ============================================================================
INSERT INTO projects (id, lgu_id, title, description, category, status, contractor, approved_budget, contract_amount, actual_cost, start_date, target_end_date, actual_end_date, latitude, longitude, address, philgeps_ref, source_document_id, fiscal_year) VALUES
    -- Manila projects
    (1,  1, 'Manila General Hospital Expansion Building',
        'Construction of new 8-storey hospital building with 200-bed capacity.',
        'Health', 'ongoing', 'DMCI Holdings Inc.',
        850000000.00, 823500000.00, NULL,
        '2023-06-01', '2025-12-31', NULL,
        14.5930, 120.9820, 'Taft Avenue, Ermita, Manila',
        'PH-GEPS-2023-0012345', 5, 2023),

    (2,  1, 'Manila Baywalk Phase 3 Rehabilitation',
        'Extension and rehabilitation of Manila Baywalk promenade from CCP to MOA.',
        'Infrastructure', 'completed', 'Megawide Construction Corp.',
        320000000.00, 315000000.00, 310500000.00,
        '2023-01-15', '2024-06-30', '2024-05-28',
        14.5505, 120.9812, 'Roxas Boulevard, Manila',
        'PH-GEPS-2022-0098712', 1, 2023),

    (3,  1, 'Manila Public School Building Renovation Batch 5',
        'Renovation of 45 public school buildings in Districts 1-3.',
        'Education', 'ongoing', 'EEI Corporation',
        180000000.00, 175200000.00, NULL,
        '2024-03-01', '2025-08-31', NULL,
        14.6050, 120.9900, 'Various locations, Manila Districts 1-3',
        'PH-GEPS-2024-0034567', 1, 2024),

    -- QC projects
    (4,  2, 'Commonwealth Avenue Protected Bike Lane',
        'Construction of 4km elevated protected bike lane along Commonwealth Avenue.',
        'Infrastructure', 'completed', 'D.M. Consunji Inc.',
        95000000.00, 92300000.00, 91800000.00,
        '2023-04-01', '2024-03-31', '2024-02-15',
        14.6870, 121.0580, 'Commonwealth Avenue, Quezon City',
        'PH-GEPS-2023-0023456', 2, 2023),

    (5,  2, 'QC Public Market Modernization - Balintawak',
        'Full renovation and modernization of Balintawak Public Market.',
        'Infrastructure', 'ongoing', 'Hilmarc''s Construction Corp.',
        250000000.00, 243000000.00, NULL,
        '2024-01-15', '2025-06-30', NULL,
        14.6570, 121.0040, 'A. Bonifacio Avenue, Balintawak, QC',
        'PH-GEPS-2023-0045678', 7, 2024),

    -- Cebu projects
    (6,  15, 'SRP Commercial Complex Phase 2A',
        'Land reclamation and commercial lot development in South Road Properties.',
        'Infrastructure', 'ongoing', 'Cebu Landmasters Inc.',
        1200000000.00, 1150000000.00, NULL,
        '2023-09-01', '2026-03-31', NULL,
        10.2870, 123.8770, 'South Road Properties, Cebu City',
        'PH-GEPS-2023-0067890', 3, 2023),

    (7,  15, 'Cebu City Flood Control - Guadalupe River',
        'Construction of flood walls and pumping stations along Guadalupe River.',
        'Infrastructure', 'completed', 'J.D. Legaspi Construction',
        185000000.00, 180000000.00, 178500000.00,
        '2023-03-01', '2024-09-30', '2024-10-15',
        10.3050, 123.9050, 'Guadalupe, Cebu City',
        'PH-GEPS-2023-0078901', 3, 2023),

    (8,  15, 'Cebu City Student Shuttle Depot',
        'Construction of bus depot and maintenance facility for student shuttle program.',
        'Education', 'completed', 'Monolith Construction & Dev.',
        45000000.00, 43800000.00, 43200000.00,
        '2023-01-10', '2023-05-31', '2023-06-15',
        10.3100, 123.8900, 'N. Bacalso Avenue, Cebu City',
        'PH-GEPS-2022-0089012', 8, 2023),

    -- Davao projects
    (9,  20, 'Davao Upland Water System Phase 3',
        'Water pipeline extension to 15 upland barangays in Calinan and Marilog districts.',
        'Infrastructure', 'ongoing', 'Davao Water District Consortium',
        420000000.00, 408000000.00, NULL,
        '2024-02-01', '2025-12-31', NULL,
        7.1500, 125.4500, 'Calinan District, Davao City',
        'PH-GEPS-2024-0012345', 9, 2024),

    (10, 20, 'Buhangin Sports Complex',
        'Construction of multi-sport complex with Olympic-sized pool and indoor courts.',
        'Recreation', 'completed', 'F.F. Cruz & Co. Inc.',
        380000000.00, 372000000.00, 368000000.00,
        '2023-05-01', '2024-11-30', '2024-12-20',
        7.1050, 125.6200, 'Buhangin, Davao City',
        'PH-GEPS-2023-0056789', 4, 2023),

    -- Makati projects
    (11, 3, 'Makati Yellow Card Wellness Center',
        'Construction of new primary care wellness center for Yellow Card holders.',
        'Health', 'completed', 'W.V. Coscolluela & Associates',
        120000000.00, 116000000.00, 114500000.00,
        '2023-07-01', '2024-04-30', '2024-04-25',
        14.5520, 121.0280, 'J.P. Rizal Extension, Makati City',
        'PH-GEPS-2023-0034567', 6, 2023),

    (12, 3, 'Makati Social Housing Project Site C',
        'Construction of 400-unit mid-rise social housing building.',
        'Housing', 'ongoing', 'DMCI Project Developers Inc.',
        680000000.00, 665000000.00, NULL,
        '2024-06-01', '2026-03-31', NULL,
        14.5450, 121.0150, 'Brgy. Comembo, Makati City',
        'PH-GEPS-2024-0045678', 10, 2024),

    (13, 3, 'Makati Digital Governance Portal Development',
        'Development and deployment of comprehensive e-governance platform.',
        'Technology', 'completed', 'Exist Software Labs Inc.',
        35000000.00, 33800000.00, 33500000.00,
        '2023-03-01', '2024-02-28', '2024-02-20',
        14.5547, 121.0244, 'Makati City Hall, Makati City',
        'PH-GEPS-2023-0023456', 6, 2023),

    -- Cross-region projects
    (14, 9, 'Baguio City Drainage Improvement',
        'Rehabilitation of drainage system in Session Road and surrounding areas.',
        'Infrastructure', 'delayed', 'North Luzon Construction Inc.',
        78000000.00, 75500000.00, NULL,
        '2024-01-15', '2024-12-31', NULL,
        16.4110, 120.5970, 'Session Road, Baguio City',
        'PH-GEPS-2023-0090123', NULL, 2024),

    (15, 22, 'CDO River Promenade Development',
        'Construction of 2km riverside promenade along Cagayan de Oro River.',
        'Infrastructure', 'bidding', NULL,
        150000000.00, NULL, NULL,
        '2025-06-01', '2026-12-31', NULL,
        8.4500, 124.6350, 'Cagayan de Oro River, CDO',
        'PH-GEPS-2025-0001234', NULL, 2025);

SELECT setval('projects_id_seq', 15);

-- ============================================================================
-- 8. BUDGET ALLOCATIONS (across 5 LGUs, multiple categories)
-- ============================================================================
INSERT INTO budget_allocations (id, lgu_id, fiscal_year, category, subcategory, allocated_amount, released_amount, utilized_amount, source_document_id) VALUES
    -- Manila FY2024
    (1,  1, 2024, 'Infrastructure',    'Roads and Bridges',        2500000000.00, 2200000000.00, 1800000000.00, 1),
    (2,  1, 2024, 'Infrastructure',    'Flood Control',            800000000.00,  750000000.00,  620000000.00,  1),
    (3,  1, 2024, 'Health',            'Hospital Operations',      1800000000.00, 1800000000.00, 1650000000.00, 1),
    (4,  1, 2024, 'Health',            'Primary Health Care',      450000000.00,  430000000.00,  390000000.00,  1),
    (5,  1, 2024, 'Education',         'School Building Program',  950000000.00,  900000000.00,  780000000.00,  1),
    (6,  1, 2024, 'Education',         'Scholarship Programs',     200000000.00,  200000000.00,  195000000.00,  1),
    (7,  1, 2024, 'Social Services',   'Housing Program',          600000000.00,  500000000.00,  350000000.00,  1),
    (8,  1, 2024, 'Environment',       'Waste Management',         350000000.00,  340000000.00,  330000000.00,  1),

    -- QC FY2024
    (9,  2, 2024, 'Infrastructure',    'Roads and Bridges',        3200000000.00, 2900000000.00, 2400000000.00, 2),
    (10, 2, 2024, 'Infrastructure',    'Bike Lane Network',        120000000.00,  120000000.00,  115000000.00,  2),
    (11, 2, 2024, 'Health',            'Hospital Operations',      1500000000.00, 1450000000.00, 1380000000.00, NULL),
    (12, 2, 2024, 'Education',         'QCU Expansion',            800000000.00,  780000000.00,  750000000.00,  NULL),
    (13, 2, 2024, 'Education',         'School Building Program',  650000000.00,  600000000.00,  520000000.00,  NULL),
    (14, 2, 2024, 'Social Services',   'Cash Aid Program',         400000000.00,  400000000.00,  395000000.00,  NULL),
    (15, 2, 2024, 'Environment',       'Urban Greening',           80000000.00,   75000000.00,   68000000.00,   NULL),

    -- Cebu City FY2024
    (16, 15, 2024, 'Infrastructure',   'SRP Development',          1500000000.00, 1200000000.00, 980000000.00,  3),
    (17, 15, 2024, 'Infrastructure',   'Flood Control',            350000000.00,  340000000.00,  310000000.00,  3),
    (18, 15, 2024, 'Health',           'Hospital Operations',      900000000.00,  880000000.00,  830000000.00,  NULL),
    (19, 15, 2024, 'Education',        'Scholarship Programs',     150000000.00,  150000000.00,  142000000.00,  NULL),
    (20, 15, 2024, 'Education',        'Student Shuttle Program',  65000000.00,   65000000.00,   62000000.00,   NULL),
    (21, 15, 2024, 'Social Services',  'Senior Citizen Benefits',  120000000.00,  115000000.00,  108000000.00,  NULL),
    (22, 15, 2024, 'Environment',      'Coastal Cleanup',          25000000.00,   23000000.00,   20000000.00,   NULL),

    -- Davao City FY2024
    (23, 20, 2024, 'Infrastructure',   'Water Systems',            600000000.00,  550000000.00,  420000000.00,  4),
    (24, 20, 2024, 'Infrastructure',   'Roads and Bridges',        1800000000.00, 1650000000.00, 1400000000.00, 4),
    (25, 20, 2024, 'Health',           'Rural Health Units',       450000000.00,  440000000.00,  410000000.00,  4),
    (26, 20, 2024, 'Education',        'School Building Program',  500000000.00,  480000000.00,  430000000.00,  NULL),
    (27, 20, 2024, 'Social Services',  'Housing Program',          350000000.00,  300000000.00,  250000000.00,  NULL),
    (28, 20, 2024, 'Environment',      'Watershed Protection',     180000000.00,  170000000.00,  155000000.00,  NULL),
    (29, 20, 2024, 'Public Safety',    'CCTV and Peacekeeping',    220000000.00,  220000000.00,  215000000.00,  NULL),

    -- Makati FY2025
    (30, 3, 2025, 'Infrastructure',    'Roads and Drainage',       1200000000.00, 800000000.00,  450000000.00,  10),
    (31, 3, 2025, 'Health',           'Yellow Card Program',       850000000.00,  820000000.00,  650000000.00,  10),
    (32, 3, 2025, 'Health',           'Wellness Centers',          200000000.00,  180000000.00,  120000000.00,  10),
    (33, 3, 2025, 'Education',        'Scholarship Programs',      300000000.00,  290000000.00,  220000000.00,  10),
    (34, 3, 2025, 'Social Services',  'Housing Program',           900000000.00,  600000000.00,  350000000.00,  10),
    (35, 3, 2025, 'Environment',      'Parks and Open Spaces',     150000000.00,  130000000.00,  85000000.00,   10),
    (36, 3, 2025, 'Technology',       'Digital Governance',         50000000.00,   48000000.00,   42000000.00,   10);

SELECT setval('budget_allocations_id_seq', 36);

-- ============================================================================
-- 9. PROMISE EVIDENCE (linking promises to projects/documents/budgets)
-- ============================================================================
INSERT INTO promise_evidence (id, promise_id, evidence_type, project_id, document_id, budget_id, report_id, external_url, notes) VALUES
    (1,  1,  'project',  1,    NULL, NULL, NULL, NULL, 'Manila General Hospital Expansion is evidence of hospital-building promise.'),
    (2,  1,  'document', NULL, 5,    NULL, NULL, NULL, 'Press release announcing hospital construction program.'),
    (3,  2,  'project',  3,    NULL, NULL, NULL, NULL, 'School renovation batch 5 is part of the rehabilitation promise.'),
    (4,  2,  'budget',   NULL, NULL, 5,    NULL, NULL, 'Education budget allocated for school building program.'),
    (5,  4,  'external_link', NULL, NULL, NULL, NULL, 'https://manila.gov.ph/free-wifi-program', 'Official page for Manila Free Wi-Fi program.'),
    (6,  6,  'project',  4,    NULL, NULL, NULL, NULL, 'Commonwealth bike lane project is direct fulfillment.'),
    (7,  6,  'budget',   NULL, NULL, 10,   NULL, NULL, 'Bike lane network budget allocation in QC.'),
    (8,  8,  'budget',   NULL, NULL, 12,   NULL, NULL, 'QCU expansion budget supports free college education.'),
    (9,  11, 'project',  6,    NULL, NULL, NULL, NULL, 'SRP Phase 2A commercial complex is part of this promise.'),
    (10, 13, 'project',  7,    NULL, NULL, NULL, NULL, 'Guadalupe River flood control project as evidence.'),
    (11, 14, 'project',  8,    NULL, NULL, NULL, NULL, 'Student shuttle depot supports the shuttle service promise.'),
    (12, 15, 'project',  9,    NULL, NULL, NULL, NULL, 'Upland water system project directly supports this promise.'),
    (13, 17, 'project',  10,   NULL, NULL, NULL, NULL, 'Buhangin sports complex is the only completed complex.'),
    (14, 19, 'project',  11,   NULL, NULL, NULL, NULL, 'Wellness center built for Yellow Card expansion.'),
    (15, 19, 'budget',   NULL, NULL, 31,   NULL, NULL, 'Yellow Card program budget allocation.'),
    (16, 20, 'project',  12,   NULL, NULL, NULL, NULL, 'Social housing project Site C supports this promise.'),
    (17, 21, 'project',  13,   NULL, NULL, NULL, NULL, 'Digital governance portal development project.');

SELECT setval('promise_evidence_id_seq', 17);

-- ============================================================================
-- 10. USERS (sample users for community reports)
-- ============================================================================
INSERT INTO users (id, email, display_name, home_lgu_id, home_region_id, role, is_verified, onboarding_completed) VALUES
    (1, 'juan.delacruz@email.com',    'Juan dela Cruz',     1,  1,  'citizen',   true, true),
    (2, 'maria.clara@email.com',      'Maria Clara',        2,  1,  'citizen',   true, true),
    (3, 'admin@sipatgov.ph',          'SipatGov Admin',     NULL, NULL, 'admin', true, true),
    (4, 'mod.visayas@sipatgov.ph',    'Visayas Moderator',  15, 10, 'moderator', true, true),
    (5, 'pedro.santos@email.com',     'Pedro Santos',       20, 14, 'citizen',   true, true);

SELECT setval('users_id_seq', 5);

-- ============================================================================
-- 11. COMMUNITY REPORTS (sample reports)
-- ============================================================================
INSERT INTO community_reports (id, user_id, lgu_id, project_id, title, description, report_type, status, latitude, longitude, address, upvote_count, is_anonymous) VALUES
    (1, 1, 1, 2,
        'Baywalk Phase 3 looks great!',
        'Just visited the new Baywalk extension. The promenade is well-maintained and the lighting is excellent. Great job by the city!',
        'feedback', 'verified',
        14.5505, 120.9812, 'Roxas Boulevard, Manila',
        42, false),

    (2, 2, 2, 5,
        'Balintawak Market renovation causing traffic',
        'The ongoing renovation of Balintawak Market is causing severe traffic congestion. Vendors are blocking adjacent roads. Needs better traffic management.',
        'concern', 'under_review',
        14.6570, 121.0040, 'A. Bonifacio Avenue, Balintawak, QC',
        28, false),

    (3, 1, 1, NULL,
        'Garbage collection missed in Tondo',
        'Garbage collection has been irregular in Barangay 20, Tondo for the past two weeks. Despite the mayor promise of twice daily collection.',
        'concern', 'submitted',
        14.6128, 120.9670, 'Tondo, Manila',
        15, false),

    (4, 5, 20, 9,
        'Water pipe construction update from Calinan',
        'The water pipe construction in Barangay Calinan is progressing well. Workers are on site daily. Expecting water connection by Q3.',
        'progress_update', 'verified',
        7.1500, 125.4500, 'Calinan, Davao City',
        33, false),

    (5, 2, 2, NULL,
        'Suspicious procurement in QC market project',
        'There appears to be a discrepancy between the posted budget and the actual materials being used in the market renovation. The tiles being installed appear to be much cheaper than what was specified.',
        'corruption_tip', 'under_review',
        14.6570, 121.0040, 'Balintawak Market, QC',
        67, true);

SELECT setval('community_reports_id_seq', 5);

-- ============================================================================
-- 12. REPORT UPVOTES
-- ============================================================================
INSERT INTO report_upvotes (user_id, report_id) VALUES
    (1, 2),
    (1, 4),
    (2, 1),
    (2, 4),
    (5, 1),
    (5, 2),
    (5, 5);

-- ============================================================================
-- 13. CRAWL JOBS (sample crawl history)
-- ============================================================================
INSERT INTO crawl_jobs (id, spider_name, status, items_scraped, items_failed, started_at, finished_at) VALUES
    (1, 'philgeps_spider',  'completed', 156, 3,  '2025-03-01 02:00:00+08', '2025-03-01 04:30:00+08'),
    (2, 'dbm_spider',       'completed', 42,  0,  '2025-03-01 05:00:00+08', '2025-03-01 05:45:00+08'),
    (3, 'coa_spider',       'completed', 28,  1,  '2025-03-02 02:00:00+08', '2025-03-02 03:15:00+08');

SELECT setval('crawl_jobs_id_seq', 3);

-- ============================================================================
-- REFRESH MATERIALIZED VIEW
-- ============================================================================
REFRESH MATERIALIZED VIEW mv_promise_stats;

COMMIT;
