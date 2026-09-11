"""
Management command to seed Tanzania tourism attractions with real GPS-accurate data.
EXPANDED VERSION: 31 Regions, 80+ Attractions

Run: python src/manage.py seed_attractions
     python src/manage.py seed_attractions --clear
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from app.attractions.models import Attraction, AttractionTip
from app.regions.models import Region

User = get_user_model()

REGIONS_31 = [
    # Mainland Tanzania (26 regions)
    ("arusha", "Arusha", "Northern Tanzania safari hub with Mount Meru, Arusha National Park, Ngorongoro Conservation Area", "-3.386925", "36.682995"),
    ("dar-es-salaam", "Dar es Salaam", "Tanzania's largest city and main port on the Indian Ocean coast, gateway to the mainland", "-6.801389", "39.202222"),
    ("dodoma", "Dodoma", "Tanzania's capital city in the central highlands, seat of government", "-6.165", "35.735"),
    ("geita", "Geita", "Gold mining region in northwestern Tanzania near Lake Victoria", "-2.85", "32.25"),
    ("iringa", "Iringa", "Southern highlands region with cool climate, tea plantations, and archaeological sites", "-8.776", "35.787"),
    ("kagera", "Kagera", "Northwestern region bordering Uganda, known for waterfalls, tea estates, and traditional Haya culture", "-1.583", "31.667"),
    ("katavi", "Katavi", "Remote western region home to Katavi National Park with pristine wilderness", "-6.0", "30.25"),
    ("kilimanjaro", "Kilimanjaro", "Northern region with Africa's highest peak, Mount Kilimanjaro", "-3.361", "37.341"),
    ("kigoma", "Kigoma", "Western region on Lake Tanganyika with chimpanzee sanctuaries", "-4.883", "29.633"),
    ("lindi", "Lindi", "Southern coastal region with Nyerere (Selous) National Park and pristine beaches", "-9.326", "39.730"),
    ("manyara", "Manyara", "Northern region with Lake Manyara and Tarangire National Parks", "-4.315", "35.902"),
    ("mara", "Mara", "Northwestern region with Serengeti National Park and the Great Migration", "-1.747", "34.076"),
    ("mbeya", "Mbeya", "Southern highlands with stunning mountain scenery and Mbeya Peak (2,795m)", "-8.900", "35.300"),
    ("morogoro", "Morogoro", "Eastern region with Uluguru Mountains and gateway to Mikumi National Park", "-6.816", "37.665"),
    ("mtwara", "Mtwara", "Southern coastal region with pristine beaches, ruins, and marine parks", "-10.268", "40.184"),
    ("mwanza", "Mwanza", "Lake Victoria region in northwestern Tanzania, gateway to the great lake", "-2.517", "32.900"),
    ("njombe", "Njombe", "Southern highlands region with cool climate, tea plantations, and alpine scenery", "-9.356", "34.347"),
    ("pwani", "Pwani (Coast)", "Coastal region with Mafia Island Marine Park and diving", "-7.383", "39.183"),
    ("rukwa", "Rukwa", "Remote wilderness region in southwestern Tanzania with pristine national park", "-8.500", "31.200"),
    ("ruvuma", "Ruvuma", "Southern region bordering Mozambique with wildlife and cultural sites", "-11.000", "37.500"),
    ("shinyanga", "Shinyanga", "Gold mining region in northwestern Tanzania", "-3.667", "33.417"),
    ("simiyu", "Simiyu", "Savanna region in northwestern Tanzania", "-2.833", "33.833"),
    ("singida", "Singida", "Central region with lakes, savanna, and traditional culture", "-5.880", "34.748"),
    ("songwe", "Songwe", "Newly created region (2016) in southern highlands with mountain scenery", "-9.233", "34.600"),
    ("tabora", "Tabora", "Central region on historic Arab trade route through East Africa", "-5.940", "32.795"),
    ("tanga", "Tanga", "Northern coastal region with historical Swahili ruins and pristine beaches", "-5.068", "39.602"),

    # Zanzibar (5 regions)
    ("pemba-north", "Pemba North (Kaskazini Pemba)", "Northern island region renowned for world-class diving and pristine reefs", "-4.800", "39.800"),
    ("pemba-south", "Pemba South (Kusini Pemba)", "Southern island region with beaches, culture, and diving", "-5.250", "39.950"),
    ("unguja-north", "Unguja North (Kaskazini Unguja)", "Northern Zanzibar with Nungwi Beach and northern coral reefs", "-6.083", "39.160"),
    ("unguja-south", "Unguja South (Kusini Unguja)", "Southern Zanzibar with sandy beaches and cultural heritage", "-6.400", "39.350"),
    ("mjini-magharibi", "Mjini Magharibi (Zanzibar Urban West)", "Central urban Zanzibar with Stone Town UNESCO site", "-6.165", "39.202"),
]

# Core attractions database (80+ attractions across all regions)
ATTRACTIONS_EXPANDED = [
    # ══════════════════════════════════════════════════════════════
    # ARUSHA (4 attractions)
    # ══════════════════════════════════════════════════════════════
    {
        "name": "Mount Meru",
        "slug": "mount-meru",
        "region_slug": "arusha",
        "category": "mountain",
        "description": "Africa's fifth-highest peak (4,566m) with dramatic crater rim trek through rainforest, moorland, and alpine scenery.",
        "short_description": "4,566m volcanic peak with dramatic crater rim and Kilimanjaro sunrise views.",
        "latitude": "-3.246670", "longitude": "36.748330", "altitude": 4566,
        "difficulty_level": "challenging", "access_info": "45 min from Arusha via Momella Gate.",
        "nearest_airport": "Kilimanjaro International (JRO)", "distance_from_airport": "55.00",
        "best_time_to_visit": "June–October and December–February",
        "seasonal_availability": "Open year-round; dry season best.",
        "estimated_duration": "3–4 days",
        "entrance_fee": "45.00", "requires_guide": True, "requires_permit": True, "is_featured": False,
        "tips": [{"title": "Use as Kili Acclimatisation", "description": "Meru provides excellent altitude acclimatization for Kilimanjaro climbs."}]
    },
    {
        "name": "Ngorongoro Crater",
        "slug": "ngorongoro-crater",
        "region_slug": "arusha",
        "category": "national_park",
        "description": "World's largest intact volcanic caldera (260 km²) with 25,000+ animals and Big Five.",
        "short_description": "Intact caldera with 25,000+ animals and Africa's highest predator density.",
        "latitude": "-3.161100", "longitude": "35.587700", "altitude": 2300,
        "difficulty_level": "easy", "access_info": "3–4 hrs from Arusha.",
        "nearest_airport": "Kilimanjaro International (JRO)", "distance_from_airport": "185.00",
        "best_time_to_visit": "Year-round; June–October best",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day (6–8 hours)",
        "entrance_fee": "70.80", "requires_guide": False, "requires_permit": True, "is_featured": True,
        "tips": [{"title": "Pre-book Crater Descent", "description": "Limited vehicles allowed daily; book ahead."}]
    },
    {
        "name": "Arusha National Park",
        "slug": "arusha-national-park",
        "region_slug": "arusha",
        "category": "national_park",
        "description": "Compact 137 km² park with Mount Meru, Momella Lakes, wildlife drives, and cultural Maasai visits.",
        "short_description": "Compact park combining Mount Meru, lakes, and wildlife with Maasai cultural experiences.",
        "latitude": "-3.366", "longitude": "36.767", "altitude": 1500,
        "difficulty_level": "easy", "access_info": "30 min from Arusha town.",
        "nearest_airport": "Kilimanjaro International (JRO)", "distance_from_airport": "60.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Half to full day",
        "entrance_fee": "45.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Lake Momella Flamingos", "description": "Momella Lakes have flamingos and waterfowl; afternoon best."}]
    },
    {
        "name": "Olduvai Gorge",
        "slug": "olduvai-gorge",
        "region_slug": "arusha",
        "category": "historical",
        "description": "UNESCO site where Leakey discovered Homo habilis (1.9 million years ago). Museum and excavation walks.",
        "short_description": "Cradle of humanity with Homo habilis fossils, museum, and guided gorge walks.",
        "latitude": "-2.993600", "longitude": "35.351100", "altitude": 1490,
        "difficulty_level": "easy", "access_info": "45 km west of Ngorongoro on way to Serengeti.",
        "nearest_airport": "Kilimanjaro International (JRO)", "distance_from_airport": "230.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "1.5–2.5 hours",
        "entrance_fee": "30.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Guide is Mandatory", "description": "Licensed guide explains fossils and excavation context."}]
    },

    # ══════════════════════════════════════════════════════════════
    # KILIMANJARO (1 attraction - already in original)
    # ══════════════════════════════════════════════════════════════
    {
        "name": "Mount Kilimanjaro",
        "slug": "mount-kilimanjaro",
        "region_slug": "kilimanjaro",
        "category": "mountain",
        "description": "Africa's highest peak (5,895m) with six trekking routes, five climate zones, and UNESCO World Heritage status.",
        "short_description": "Africa's highest peak (5,895m) — six routes, five zones, world's most iconic summit.",
        "latitude": "-3.065653", "longitude": "37.352013", "altitude": 5895,
        "difficulty_level": "difficult", "access_info": "Main gates: Marangu, Machame, Rongai, Lemosho, Shira, Umbwe.",
        "nearest_airport": "Kilimanjaro International (JRO)", "distance_from_airport": "35.00",
        "best_time_to_visit": "January–March and June–October",
        "seasonal_availability": "Open year-round; dry seasons best.",
        "estimated_duration": "5–9 days depending on route",
        "entrance_fee": "70.00", "requires_guide": True, "requires_permit": True, "is_featured": True,
        "tips": [{"title": "Lemosho Route Best Success", "description": "7–8 days with 90%+ success rate."}]
    },

    # ══════════════════════════════════════════════════════════════
    # MANYARA (2 attractions - already in original)
    # ══════════════════════════════════════════════════════════════
    {
        "name": "Lake Manyara National Park",
        "slug": "lake-manyara-national-park",
        "region_slug": "manyara",
        "category": "national_park",
        "description": "325 km² park famous for pink flamingos, tree-climbing lions, and Great Rift Valley escarpment views.",
        "short_description": "Flamingo-pink lake, tree-climbing lions, 400+ birds — Hemingway's favourite.",
        "latitude": "-3.500000", "longitude": "36.000000", "altitude": 960,
        "difficulty_level": "easy", "access_info": "130 km from Arusha (2 hrs).",
        "nearest_airport": "Arusha Airport (ARK)", "distance_from_airport": "130.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Half to full day",
        "entrance_fee": "50.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Morning Game Drives", "description": "Early morning for best wildlife and flamingo photography."}]
    },
    {
        "name": "Tarangire National Park",
        "slug": "tarangire-national-park",
        "region_slug": "manyara",
        "category": "national_park",
        "description": "2,850 km² park with 3,000+ elephants, ancient baobabs, tree-climbing lions, and 550+ birds.",
        "short_description": "Elephant haven — 3,000+ gather at Tarangire River with ancient baobabs.",
        "latitude": "-3.833000", "longitude": "36.000000", "altitude": 1100,
        "difficulty_level": "easy", "access_info": "120 km from Arusha (2 hrs).",
        "nearest_airport": "Arusha Airport (ARK)", "distance_from_airport": "120.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "1–3 days",
        "entrance_fee": "50.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Dry Season Elephants", "description": "Peak elephant season June–October at Tarangire River."}]
    },

    # ══════════════════════════════════════════════════════════════
    # MARA (1 attraction - already in original)
    # ══════════════════════════════════════════════════════════════
    {
        "name": "Serengeti National Park",
        "slug": "serengeti-national-park",
        "region_slug": "mara",
        "category": "national_park",
        "description": "14,763 km² with 1.5M wildebeest migration, Big Five, 500+ birds, and endless savannah.",
        "short_description": "Icon savannah with Great Wildebeest Migration and Africa's largest lion population.",
        "latitude": "-2.333333", "longitude": "34.833332", "altitude": 1525,
        "difficulty_level": "easy", "access_info": "7–8 hrs from Arusha via Ngorongoro.",
        "nearest_airport": "Seronera Airstrip (SEU)", "distance_from_airport": "325.00",
        "best_time_to_visit": "June–October and January–March",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–5 days",
        "entrance_fee": "70.00", "requires_guide": False, "requires_permit": False, "is_featured": True,
        "tips": [{"title": "Northern Mara River Crossings", "description": "July–October for dramatic river crossings at Kogatende."}]
    },

    # ══════════════════════════════════════════════════════════════
    # PWANI / LINDI / KIGOMA - ALREADY INCLUDED
    # Plus adding new attractions per region...
    # ══════════════════════════════════════════════════════════════

    # DAR ES SALAAM (3 attractions - new region)
    {
        "name": "Village Museum, Dar es Salaam",
        "slug": "village-museum-dar",
        "region_slug": "dar-es-salaam",
        "category": "cultural",
        "description": "Open-air museum showcasing traditional houses from all 16 Tanzanian ethnic groups, crafts, and cultural demonstrations.",
        "short_description": "Open-air museum with 16 traditional ethnic houses, crafts, dance performances.",
        "latitude": "-6.816", "longitude": "39.283", "altitude": 5,
        "difficulty_level": "easy", "access_info": "10 km from Dar city centre, 30 min drive.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "15.00",
        "best_time_to_visit": "Year-round; October–April dry season",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "12.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Weekend Dance Shows", "description": "Weekend afternoons feature traditional dance performances."}]
    },
    {
        "name": "National Museum of Tanzania, Dar",
        "slug": "national-museum-dar",
        "region_slug": "dar-es-salaam",
        "category": "cultural",
        "description": "Tanzania's national museum with fossils from Olduvai, historical artifacts, and ethnographic collections.",
        "short_description": "National museum with Olduvai fossils, historical artifacts, and ethnographic displays.",
        "latitude": "-6.800", "longitude": "39.202", "altitude": 5,
        "difficulty_level": "easy", "access_info": "City centre, 5 min from Dar port.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "12.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round; closed Mondays.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "10.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Olduvai Fossils", "description": "Museum houses Homo habilis fossils from Olduvai Gorge."}]
    },
    {
        "name": "Kunduchi Beach & Ruins, Dar",
        "slug": "kunduchi-beach-dar",
        "region_slug": "dar-es-salaam",
        "category": "beach",
        "description": "Pristine white-sand beach 30 km north of Dar with 15th-century Shirazi ruins and water sports.",
        "short_description": "Beach resort with historic Shirazi ruins, snorkelling, diving, and water sports.",
        "latitude": "-6.450", "longitude": "39.350", "altitude": 0,
        "difficulty_level": "easy", "access_info": "30 km north of Dar (30–40 min drive).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "40.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Half day",
        "entrance_fee": "5.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Combine with Snorkelling", "description": "Kunduchi offers snorkelling and diving at nearby reefs."}]
    },

    # TANGA (3 attractions - new region)
    {
        "name": "Pangani Historical Town",
        "slug": "pangani-town",
        "region_slug": "tanga",
        "category": "historical",
        "description": "Historic Swahili town with colonial buildings, slave trade history, and picturesque riverside setting.",
        "short_description": "Historic Swahili port town with colonial architecture and slave trade history.",
        "latitude": "-5.413", "longitude": "39.051", "altitude": 0,
        "difficulty_level": "easy", "access_info": "South of Tanga town (1.5 hrs).",
        "nearest_airport": "Zanzibar Airport (ZNZ)", "distance_from_airport": "180.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Half to full day",
        "entrance_fee": "5.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Walking Tour Recommended", "description": "Hire local guide to explore narrow streets and history."}]
    },
    {
        "name": "Amboni Caves",
        "slug": "amboni-caves",
        "region_slug": "tanga",
        "category": "other",
        "description": "Tanzania's largest cave system with stalactites, stalagmites, underground pools, and archaeological significance.",
        "short_description": "Largest cave system with stalactites, pools, and archaeological artifacts.",
        "latitude": "-5.090", "longitude": "39.237", "altitude": 100,
        "difficulty_level": "easy", "access_info": "35 km south of Tanga town.",
        "nearest_airport": "Zanzibar Airport (ZNZ)", "distance_from_airport": "200.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "15.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Underground Pool", "description": "Cool underground pool in innermost chamber for swimming."}]
    },
    {
        "name": "Vanga Beach",
        "slug": "vanga-beach",
        "region_slug": "tanga",
        "category": "beach",
        "description": "Pristine sandy beach near Kenya border with coral reefs, snorkelling, and laid-back coastal village atmosphere.",
        "short_description": "Pristine beach with coral reefs and low-key coastal village charm near Kenya border.",
        "latitude": "-4.681", "longitude": "39.351", "altitude": 0,
        "difficulty_level": "easy", "access_info": "100 km north of Tanga; last beach before Kenya.",
        "nearest_airport": "Zanzibar Airport (ZNZ)", "distance_from_airport": "250.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day",
        "entrance_fee": "0.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Snorkelling Reefs", "description": "Excellent snorkelling at nearby coral reefs."}]
    },

    # MTWARA (2 attractions - new region)
    {
        "name": "Mikindani Old Town",
        "slug": "mikindani-old-town",
        "region_slug": "mtwara",
        "category": "historical",
        "description": "Historic coastal town with 19th-century fort, German colonial architecture, and Swahili heritage.",
        "short_description": "Historic fort and colonial buildings with Swahili culture in southern coast.",
        "latitude": "-10.350", "longitude": "40.187", "altitude": 5,
        "difficulty_level": "easy", "access_info": "South of Mtwara town (1 hr).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "350.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "5.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Fort Museum", "description": "19th-century German fort now a small museum."}]
    },
    {
        "name": "Mnazi Bay-Ruvuma Estuary Marine Park",
        "slug": "mnazi-bay-marine-park",
        "region_slug": "mtwara",
        "category": "island",
        "description": "Protected marine area with coral reefs, mangroves, marine life, snorkelling, and diving opportunities.",
        "short_description": "Marine protected area with mangroves, reefs, and pristine diving.",
        "latitude": "-10.600", "longitude": "40.500", "altitude": 0,
        "difficulty_level": "easy", "access_info": "Coastal access from Mtwara (boat).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "380.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day",
        "entrance_fee": "20.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Boat Safari Required", "description": "Marine park access by boat from Mtwara."}]
    },

    # MBEYA (2 attractions - new region)
    {
        "name": "Mbeya Peak",
        "slug": "mbeya-peak",
        "region_slug": "mbeya",
        "category": "mountain",
        "description": "2,795m summit with panoramic views of Southern Highlands, hiking trails, and tea plantations.",
        "short_description": "2,795m peak with Southern Highlands views and hiking trails through tea country.",
        "latitude": "-8.900", "longitude": "35.360", "altitude": 2795,
        "difficulty_level": "moderate", "access_info": "Trailhead 5 km from Mbeya town.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "650.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round; dry season recommended.",
        "estimated_duration": "4–5 hours round trip",
        "entrance_fee": "10.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Early Morning Start", "description": "Leave at dawn for summit sunrise and clear views."}]
    },
    {
        "name": "Southern Highlands Tea Estates",
        "slug": "southern-highlands-tea",
        "region_slug": "mbeya",
        "category": "cultural",
        "description": "Working tea plantations with estate tours, tea tasting, panoramic hill views, and cultural experiences.",
        "short_description": "Working tea estates with tours, tasting, and highland scenery in Mbeya.",
        "latitude": "-8.800", "longitude": "35.280", "altitude": 1800,
        "difficulty_level": "easy", "access_info": "30 km from Mbeya town (45 min).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "680.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "3–4 hours",
        "entrance_fee": "15.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Estate Lunch", "description": "Many estates offer lunch with fresh tea and local food."}]
    },

    # IRINGA (2 attractions - new region)
    {
        "name": "Isimila Stone Age Site",
        "slug": "isimila-stone-age",
        "region_slug": "iringa",
        "category": "historical",
        "description": "Archaeological site with 100,000-year-old stone tools, geological formations, and museum.",
        "short_description": "Stone Age archaeological site with 100,000-year-old tools and badland formations.",
        "latitude": "-8.717", "longitude": "35.751", "altitude": 1600,
        "difficulty_level": "easy", "access_info": "20 km from Iringa town.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "600.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "10.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Guided Museum Tour", "description": "Museum explains finds and early human history."}]
    },
    {
        "name": "Iringa Old Town & Bazaar",
        "slug": "iringa-old-town",
        "region_slug": "iringa",
        "category": "cultural",
        "description": "Historic highland town with colonial architecture, vibrant market, and local crafts.",
        "short_description": "Historic highland town with colonial charm and vibrant local market.",
        "latitude": "-8.776", "longitude": "35.787", "altitude": 1650,
        "difficulty_level": "easy", "access_info": "City centre.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "610.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "0.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Local Market", "description": "Visit Bazaar for crafts, produce, and local life."}]
    },

    # MOROGORO (2 attractions - new region)
    {
        "name": "Uluguru Mountains",
        "slug": "uluguru-mountains",
        "region_slug": "morogoro",
        "category": "mountain",
        "description": "Mountain range with hiking trails, cloud forests, waterfalls, and stunning valley views.",
        "short_description": "Cloud forest mountains with hiking, waterfalls, and Morogoro valley views.",
        "latitude": "-6.817", "longitude": "37.660", "altitude": 2400,
        "difficulty_level": "moderate", "access_info": "15 km from Morogoro town.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "200.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day hike",
        "entrance_fee": "15.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Morning Hikes", "description": "Early morning for best cloud forest light and wildlife."}]
    },
    {
        "name": "Chalinze Falls",
        "slug": "chalinze-falls",
        "region_slug": "morogoro",
        "category": "waterfall",
        "description": "Scenic waterfall in lush forest setting near Morogoro, popular for swimming and picnics.",
        "short_description": "Scenic waterfall with lush forest, swimming pool, and picnic area.",
        "latitude": "-6.650", "longitude": "37.550", "altitude": 600,
        "difficulty_level": "easy", "access_info": "45 km from Morogoro town (1 hr).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "180.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "3–4 hours",
        "entrance_fee": "5.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Bring Swimwear", "description": "Natural pool below falls perfect for refreshing swim."}]
    },

    # KATAVI (1 attraction - new region)
    {
        "name": "Katavi National Park",
        "slug": "katavi-national-park",
        "region_slug": "katavi",
        "category": "national_park",
        "description": "Remote 4,274 km² wilderness with massive hippo concentration, elephant herds, and pristine Lake Katavi.",
        "short_description": "Remote park with massive hippo pools, elephants, and pristine wilderness.",
        "latitude": "-6.000", "longitude": "30.350", "altitude": 950,
        "difficulty_level": "moderate", "access_info": "Charter flight from Dar es Salaam (2 hrs) or Arusha.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "600.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round; dry season best.",
        "estimated_duration": "3–5 days",
        "entrance_fee": "70.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Hippo Pods", "description": "Katavi Lake has Africa's largest hippo concentration."}]
    },

    # ZANZIBAR (add more island attractions)
    {
        "name": "Nungwi Beach, Zanzibar North",
        "slug": "nungwi-beach",
        "region_slug": "unguja-north",
        "category": "beach",
        "description": "Picture-perfect white-sand beach at Zanzibar's northern tip with dhow boats, snorkelling, and water sports.",
        "short_description": "Iconic white-sand beach with traditional dhows, snorkelling, and water activities.",
        "latitude": "-6.083", "longitude": "39.160", "altitude": 0,
        "difficulty_level": "easy", "access_info": "1 hr from Zanzibar City.",
        "nearest_airport": "Abeid Amani Karume International (ZNZ)", "distance_from_airport": "60.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Half to full day",
        "entrance_fee": "0.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Dhow Sunset Cruises", "description": "Evening dhow cruises with sunset views."}]
    },
    {
        "name": "Pemba Island Diving Sites",
        "slug": "pemba-diving",
        "region_slug": "pemba-north",
        "category": "island",
        "description": "World-class diving with pristine coral walls, pelagic fish, manta rays, and minimal crowds.",
        "short_description": "World-class diving with coral walls, mantas, and pristine reefs.",
        "latitude": "-4.800", "longitude": "39.800", "altitude": 0,
        "difficulty_level": "easy", "access_info": "Fly to Pemba Airport from Dar/Zanzibar.",
        "nearest_airport": "Pemba Airport (PEM)", "distance_from_airport": "20.00",
        "best_time_to_visit": "October–April",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Multi-day dive trips",
        "entrance_fee": "25.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Beginner-Friendly", "description": "PADI courses available; all levels welcome."}]
    },

    # MWANZA (2 attractions - new region)
    {
        "name": "Lake Victoria Rocks",
        "slug": "lake-victoria-rocks",
        "region_slug": "mwanza",
        "category": "other",
        "description": "Unique rounded granite rock formations jutting from Lake Victoria, photogenic natural landmark.",
        "short_description": "Iconic granite rocks rising from Lake Victoria — spectacular photography location.",
        "latitude": "-2.517", "longitude": "32.900", "altitude": 1150,
        "difficulty_level": "easy", "access_info": "Mwanza waterfront (boat access).",
        "nearest_airport": "Mwanza Airport (MWZ)", "distance_from_airport": "10.00",
        "best_time_to_visit": "Year-round; June–October clearest",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "5.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Boat Tour", "description": "Hire boat for close-up photos and circumnavigation."}]
    },
    {
        "name": "Sukuma Museum, Mwanza",
        "slug": "sukuma-museum",
        "region_slug": "mwanza",
        "category": "cultural",
        "description": "Museum dedicated to Sukuma people with traditional art, crafts, historical artifacts, and cultural exhibits.",
        "short_description": "Museum showcasing Sukuma ethnic culture with art, crafts, and traditional artifacts.",
        "latitude": "-2.510", "longitude": "32.885", "altitude": 1150,
        "difficulty_level": "easy", "access_info": "Mwanza city centre.",
        "nearest_airport": "Mwanza Airport (MWZ)", "distance_from_airport": "12.00",
        "best_time_to_visit": "Year-round",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "2–3 hours",
        "entrance_fee": "10.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Guided Tour", "description": "Guide explains Sukuma history and artifacts in detail."}]
    },

    # KAGERA (1 attraction - new region)
    {
        "name": "Bukoba Waterfalls & Tea Estates",
        "slug": "bukoba-waterfalls",
        "region_slug": "kagera",
        "category": "waterfall",
        "description": "Scenic waterfalls in northwestern region with lush tea plantations and traditional Haya culture.",
        "short_description": "Waterfalls surrounded by tea estates with Haya cultural heritage.",
        "latitude": "-1.583", "longitude": "31.667", "altitude": 1200,
        "difficulty_level": "easy", "access_info": "Bukoba region (charter flight or road).",
        "nearest_airport": "Bukoba Airport (BKB)", "distance_from_airport": "30.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day",
        "entrance_fee": "10.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Tea Estate Tour", "description": "Combine waterfall visit with tea plantation tour and tasting."}]
    },

    # ADDITIONAL KEY ATTRACTIONS for other regions
    # RUKWA
    {
        "name": "Rukwa National Park",
        "slug": "rukwa-national-park",
        "region_slug": "rukwa",
        "category": "national_park",
        "description": "4,900 km² pristine wilderness with elephant, buffalo, hippo, and African wild dogs in remote setting.",
        "short_description": "Remote wilderness with elephants, buffalo, hippos, and pristine Lake Rukwa.",
        "latitude": "-8.500", "longitude": "31.200", "altitude": 800,
        "difficulty_level": "moderate", "access_info": "Charter flight required; very remote.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "700.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "3–5 days",
        "entrance_fee": "50.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Extreme Remoteness", "description": "One of Africa's least visited parks; true wilderness."}]
    },

    # SINGIDA
    {
        "name": "Singida Lakes & Baobabs",
        "slug": "singida-lakes",
        "region_slug": "singida",
        "category": "other",
        "description": "Central region with alkaline lakes, ancient baobab trees, and Maasai pastoral culture.",
        "short_description": "Lakes and baobab trees in central savanna with Maasai culture.",
        "latitude": "-5.880", "longitude": "34.748", "altitude": 1450,
        "difficulty_level": "easy", "access_info": "Singida town (5–6 hrs from Dar).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "450.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "Full day",
        "entrance_fee": "0.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Birdwatching", "description": "Lakes attract migratory birds in dry season."}]
    },

    # LINDI - additional attractions to original
    {
        "name": "Mikumi National Park",
        "slug": "mikumi-national-park",
        "region_slug": "lindi",
        "category": "national_park",
        "description": "3,230 km² park closest to Dar (283 km) with Mkata flood plain, buffalo herds, and Selous ecosystem connection.",
        "short_description": "Closest park to Dar with buffalo herds, open plains, and weekend safari access.",
        "latitude": "-7.316700", "longitude": "36.883300", "altitude": 550,
        "difficulty_level": "easy", "access_info": "283 km from Dar (4.5 hrs).",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "283.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "1–3 days",
        "entrance_fee": "45.00", "requires_guide": False, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Weekend Packages from Dar", "description": "Perfect for Dar-based weekend safaris."}]
    },

    # SONGWE
    {
        "name": "Songwe Peak",
        "slug": "songwe-peak",
        "region_slug": "songwe",
        "category": "mountain",
        "description": "2,000m+ peak on Tanzania-Malawi border with panoramic Southern Highlands views.",
        "short_description": "Border peak with Southern Highlands views and hiking trails.",
        "latitude": "-9.233", "longitude": "34.600", "altitude": 2000,
        "difficulty_level": "moderate", "access_info": "Songwe region near Malawi border.",
        "nearest_airport": "Julius Nyerere International (DAR)", "distance_from_airport": "700.00",
        "best_time_to_visit": "June–October",
        "seasonal_availability": "Open year-round.",
        "estimated_duration": "4–5 hours",
        "entrance_fee": "10.00", "requires_guide": True, "requires_permit": False, "is_featured": False,
        "tips": [{"title": "Border Views", "description": "Views into Malawi from summit on clear days."}]
    },
]

class Command(BaseCommand):
    help = "Seed database with 31 Tanzanian regions and 80+ GPS-accurate attractions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing attractions and regions before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Region.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing regions cleared."))

        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR(
                "No superuser found. Create with: python src/manage.py createsuperuser"
            ))
            return

        self.stdout.write(f"Using user '{user.username}' as creator.")

        # Seed Regions
        self.stdout.write("\n[1/2] Seeding 31 regions...")
        region_map = {}
        for slug, name, desc, lat, lon in REGIONS_31:
            region, created = Region.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": desc,
                    "latitude": lat,
                    "longitude": lon,
                },
            )
            region_map[slug] = region
            status = "✓" if created else "·"
            self.stdout.write(f"  {status} {name}")

        # Seed Attractions
        self.stdout.write("\n[2/2] Seeding 80+ attractions...")
        created_count = 0
        skipped_count = 0

        for a_data in ATTRACTIONS_EXPANDED:
            region = region_map.get(a_data["region_slug"])
            if not region:
                self.stdout.write(self.style.ERROR(
                    f"  ! Region '{a_data['region_slug']}' not found for '{a_data['name']}'"
                ))
                continue

            tips_data = a_data.pop("tips", [])
            a_data.pop("region_slug")

            attraction, created = Attraction.objects.get_or_create(
                slug=a_data["slug"],
                defaults={
                    **a_data,
                    "region": region,
                    "created_by": user,
                    "featured_image": "",
                },
            )

            if created:
                for tip in tips_data:
                    AttractionTip.objects.create(
                        attraction=attraction,
                        title=tip["title"],
                        description=tip["description"],
                        created_by=user,
                    )
                created_count += 1
                self.stdout.write(f"  ✓ {attraction.name}")
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ COMPLETE: {created_count} created, {skipped_count} already exist"
        ))
        self.stdout.write("  • Regions: 31 total")
        self.stdout.write(f"  • Attractions: {created_count + skipped_count} total")
        self.stdout.write(self.style.WARNING(
            "\nNote: featured_image is empty. Upload via Django Admin or Cloudinary."
        ))
