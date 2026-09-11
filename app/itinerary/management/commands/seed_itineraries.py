from django.core.management.base import BaseCommand

from app.itinerary.models import Itinerary, ItineraryActivity, ItineraryDay

ITINERARIES = [
    {
        'title': '7 Days Northern Circuit Safari',
        'slug': '7-days-northern-circuit-safari',
        'description': 'The classic Tanzania safari covering Tarangire, Ngorongoro, and Serengeti. Good for first-time visitors who want to see the highlights of northern Tanzania.',
        'total_days': 7,
        'estimated_budget_usd': 3500,
        'difficulty_level': 'easy',
        'days': [
            {
                'day_number': 1,
                'title': 'Arrival in Arusha',
                'description': 'Arrive at Kilimanjaro International Airport. Transfer to your hotel in Arusha. Safari briefing in the evening.',
                'accommodation_notes': 'Arusha town hotel or guesthouse',
                'meals_notes': 'Dinner on own account',
                'activities': [
                    {'title': 'Airport pickup and transfer to Arusha', 'duration_hours': 2, 'order': 1},
                    {'title': 'Rest and safari briefing with your guide', 'duration_hours': 1.5, 'order': 2},
                ]
            },
            {
                'day_number': 2,
                'title': 'Tarangire National Park',
                'description': 'Drive from Arusha to Tarangire. Full day game drive. Famous for large elephant herds and ancient baobab trees.',
                'accommodation_notes': 'Tented camp near Tarangire',
                'meals_notes': 'Breakfast at hotel, lunch and dinner at camp',
                'activities': [
                    {'title': 'Drive Arusha to Tarangire (2.5 hours)', 'start_time': '07:00', 'duration_hours': 2.5, 'order': 1},
                    {'title': 'Morning game drive in Tarangire', 'start_time': '10:00', 'duration_hours': 3, 'order': 2},
                    {'title': 'Picnic lunch at Silale Swamp', 'start_time': '13:00', 'duration_hours': 1, 'order': 3},
                    {'title': 'Afternoon game drive', 'start_time': '15:00', 'duration_hours': 3, 'order': 4},
                ]
            },
            {
                'day_number': 3,
                'title': 'Lake Manyara and drive to Ngorongoro',
                'description': 'Morning game drive in Lake Manyara, known for flamingos, tree-climbing lions, and hippos. Afternoon drive up to the Ngorongoro Crater rim.',
                'accommodation_notes': 'Lodge or camp on Ngorongoro crater rim',
                'meals_notes': 'Full board',
                'activities': [
                    {'title': 'Game drive in Lake Manyara National Park', 'start_time': '07:00', 'duration_hours': 4, 'order': 1},
                    {'title': 'Drive to Ngorongoro rim', 'start_time': '14:00', 'duration_hours': 2, 'order': 2},
                    {'title': 'Sunset walk on the crater rim', 'start_time': '17:00', 'duration_hours': 1, 'order': 3},
                ]
            },
            {
                'day_number': 4,
                'title': 'Ngorongoro Crater descent',
                'description': 'Full day inside the Ngorongoro Crater. One of the best days for wildlife sightings in Tanzania — lions, black rhino, elephants, hippos, and flamingo all in one caldera.',
                'accommodation_notes': 'Return to crater rim lodge',
                'meals_notes': 'Packed breakfast and picnic lunch inside crater, dinner at lodge',
                'activities': [
                    {'title': 'Early morning descent into the crater', 'start_time': '06:30', 'duration_hours': 1, 'order': 1},
                    {'title': 'Full day game drive on crater floor', 'start_time': '07:30', 'duration_hours': 7, 'order': 2},
                    {'title': 'Picnic lunch at Hippo Pool', 'start_time': '12:30', 'duration_hours': 1, 'order': 3},
                    {'title': 'Ascent back to the rim', 'start_time': '16:00', 'duration_hours': 1, 'order': 4},
                ]
            },
            {
                'day_number': 5,
                'title': 'Drive to Serengeti via Olduvai Gorge',
                'description': 'Morning drive from Ngorongoro to the Serengeti with a stop at Olduvai Gorge, one of the most important paleoanthropology sites in the world. Afternoon game drive in the Central Serengeti.',
                'accommodation_notes': 'Camp or tented camp in Serengeti',
                'meals_notes': 'Full board',
                'activities': [
                    {'title': 'Drive from Ngorongoro to Olduvai Gorge', 'start_time': '08:00', 'duration_hours': 1.5, 'order': 1},
                    {'title': 'Guided tour of Olduvai Gorge and museum', 'start_time': '10:00', 'duration_hours': 1, 'order': 2},
                    {'title': 'Cross into Serengeti, game drive to camp', 'start_time': '12:00', 'duration_hours': 4, 'order': 3},
                ]
            },
            {
                'day_number': 6,
                'title': 'Full day in the Serengeti',
                'description': 'Full day exploring the Serengeti. Game drives in the morning and afternoon with a midday break. Location varies depending on where the migration is.',
                'accommodation_notes': 'Same camp as previous night or move to central Serengeti',
                'meals_notes': 'Full board',
                'activities': [
                    {'title': 'Early morning game drive', 'start_time': '06:00', 'duration_hours': 4, 'order': 1},
                    {'title': 'Lunch and rest at camp', 'start_time': '12:00', 'duration_hours': 2, 'order': 2},
                    {'title': 'Afternoon game drive, sunset in the Serengeti', 'start_time': '15:30', 'duration_hours': 3, 'order': 3},
                ]
            },
            {
                'day_number': 7,
                'title': 'Return to Arusha and departure',
                'description': 'Morning game drive before leaving the Serengeti. Long drive back to Arusha. Depending on flight time, there may be time to visit a local market.',
                'accommodation_notes': 'Airport hotel if needed',
                'meals_notes': 'Breakfast and lunch included',
                'activities': [
                    {'title': 'Final morning game drive', 'start_time': '06:30', 'duration_hours': 2, 'order': 1},
                    {'title': 'Drive back to Arusha (5-6 hours)', 'start_time': '10:00', 'duration_hours': 6, 'order': 2},
                    {'title': 'Transfer to Kilimanjaro Airport', 'duration_hours': 1, 'order': 3},
                ]
            },
        ]
    },
    {
        'title': '8 Days Kilimanjaro Climb via Machame Route',
        'slug': '8-days-kilimanjaro-climb-machame-route',
        'description': 'The Machame route is the most popular way to climb Kilimanjaro. This 8-day version adds an extra acclimatisation day on the Shira Plateau, significantly improving summit success rates.',
        'total_days': 8,
        'estimated_budget_usd': 2800,
        'difficulty_level': 'difficult',
        'days': [
            {
                'day_number': 1,
                'title': 'Arrive Moshi, transfer to Machame Gate',
                'description': 'Arrive in Moshi. Final gear check and briefing at your hotel. Afternoon drive to Machame Gate and begin the climb through the rainforest.',
                'accommodation_notes': 'Machame Camp (2,835m) — forest tent camp',
                'meals_notes': 'Lunch at gate, dinner at camp',
                'activities': [
                    {'title': 'Briefing and gear check in Moshi', 'duration_hours': 2, 'order': 1},
                    {'title': 'Drive to Machame Gate (45 min)', 'duration_hours': 1, 'order': 2},
                    {'title': 'Trek through rainforest to Machame Camp', 'duration_hours': 5, 'estimated_cost_usd': 0, 'order': 3},
                ]
            },
            {
                'day_number': 2,
                'title': 'Machame Camp to Shira Camp',
                'description': 'Climb from the forest zone through the moorland into the Shira Plateau. The vegetation changes dramatically and Kilimanjaro\'s summit becomes visible for the first time.',
                'accommodation_notes': 'Shira Camp (3,840m)',
                'meals_notes': 'All meals provided by camp crew',
                'activities': [
                    {'title': 'Trek from Machame Camp through moorland to Shira Plateau', 'start_time': '08:00', 'duration_hours': 6, 'order': 1},
                    {'title': 'Rest and acclimatise at Shira Camp', 'duration_hours': 2, 'order': 2},
                ]
            },
            {
                'day_number': 3,
                'title': 'Shira Camp to Lava Tower and back to Barranco',
                'description': 'Classic acclimatisation day: climb high, sleep low. Trek up to Lava Tower at 4,600m, then descend to Barranco Camp at 3,976m. This is key for acclimatisation.',
                'accommodation_notes': 'Barranco Camp (3,976m)',
                'meals_notes': 'All meals at camp',
                'activities': [
                    {'title': 'Climb to Lava Tower (4,600m)', 'start_time': '07:30', 'duration_hours': 4, 'order': 1},
                    {'title': 'Lunch at Lava Tower', 'start_time': '12:00', 'duration_hours': 1, 'order': 2},
                    {'title': 'Descend to Barranco Camp', 'start_time': '13:30', 'duration_hours': 2.5, 'order': 3},
                ]
            },
            {
                'day_number': 4,
                'title': 'Barranco to Karanga Camp',
                'description': 'The day starts with the famous Barranco Wall — a steep but non-technical scramble. Good views of the Western Breach after the climb.',
                'accommodation_notes': 'Karanga Camp (4,035m)',
                'meals_notes': 'All meals at camp',
                'activities': [
                    {'title': 'Climb the Barranco Wall', 'start_time': '07:30', 'duration_hours': 2, 'order': 1},
                    {'title': 'Trek across Karanga Valley to Karanga Camp', 'start_time': '10:00', 'duration_hours': 3, 'order': 2},
                    {'title': 'Rest and prepare gear for summit push', 'duration_hours': 2, 'order': 3},
                ]
            },
            {
                'day_number': 5,
                'title': 'Karanga to Base Camp',
                'description': 'Shorter day to allow rest before summit night. Arrive at Base Camp (Barafu) in early afternoon. Rest, eat, sleep early.',
                'accommodation_notes': 'Barafu Base Camp (4,673m)',
                'meals_notes': 'All meals at camp',
                'activities': [
                    {'title': 'Trek from Karanga to Barafu Base Camp', 'start_time': '08:00', 'duration_hours': 4, 'order': 1},
                    {'title': 'Rest, hydrate, pack summit gear', 'duration_hours': 3, 'order': 2},
                    {'title': 'Early dinner and sleep by 7pm', 'start_time': '17:00', 'duration_hours': 2, 'order': 3},
                ]
            },
            {
                'day_number': 6,
                'title': 'Summit Night and descent to Mweka Camp',
                'description': 'Midnight start for the summit push. Reach Stella Point on the crater rim at sunrise. Continue to Uhuru Peak (5,895m), the highest point in Africa. Descend all the way to Mweka Camp.',
                'accommodation_notes': 'Mweka Camp (3,100m)',
                'meals_notes': 'Hot tea and light snack before summit, full meals at Mweka',
                'activities': [
                    {'title': 'Wake up and prepare for summit', 'start_time': '23:30', 'duration_hours': 0.5, 'order': 1},
                    {'title': 'Summit push to Stella Point', 'start_time': '00:00', 'duration_hours': 6, 'order': 2},
                    {'title': 'Continue to Uhuru Peak (5,895m)', 'duration_hours': 1, 'order': 3},
                    {'title': 'Descend from summit to Barafu, then Mweka', 'duration_hours': 5, 'order': 4},
                ]
            },
            {
                'day_number': 7,
                'title': 'Mweka Camp to Mweka Gate and Moshi',
                'description': 'Final descent through the rainforest to Mweka Gate. Certificates are awarded at the gate. Transfer to Moshi for showers and celebration dinner.',
                'accommodation_notes': 'Hotel in Moshi',
                'meals_notes': 'Breakfast at camp, celebration dinner in Moshi',
                'activities': [
                    {'title': 'Trek from Mweka Camp through forest to Mweka Gate', 'start_time': '08:00', 'duration_hours': 3, 'order': 1},
                    {'title': 'Certificate presentation at Mweka Gate', 'duration_hours': 0.5, 'order': 2},
                    {'title': 'Transfer to Moshi hotel', 'duration_hours': 1, 'order': 3},
                ]
            },
            {
                'day_number': 8,
                'title': 'Departure from Moshi',
                'description': 'Rest day in Moshi. Optional visit to Moshi market or local coffee farm. Transfer to Kilimanjaro Airport for departure.',
                'accommodation_notes': 'Moshi hotel (checkout)',
                'meals_notes': 'Breakfast included',
                'activities': [
                    {'title': 'Optional Moshi town walk or coffee farm visit', 'duration_hours': 2, 'order': 1},
                    {'title': 'Transfer to Kilimanjaro Airport', 'duration_hours': 1, 'order': 2},
                ]
            },
        ]
    },
    {
        'title': '5 Days Zanzibar Beach and Culture',
        'slug': '5-days-zanzibar-beach-culture',
        'description': 'A relaxed itinerary covering Stone Town, spice farms, and the best beaches. Good for anyone who wants to combine Tanzanian culture with Indian Ocean beach time.',
        'total_days': 5,
        'estimated_budget_usd': 800,
        'difficulty_level': 'easy',
        'days': [
            {
                'day_number': 1,
                'title': 'Arrive Zanzibar, Stone Town exploration',
                'description': 'Arrive at Zanzibar International Airport. Check in to Stone Town hotel. Afternoon walk through the historic streets.',
                'accommodation_notes': 'Stone Town hotel or guesthouse',
                'meals_notes': 'Dinner at Forodhani Gardens night market',
                'activities': [
                    {'title': 'Airport transfer to Stone Town', 'duration_hours': 0.5, 'order': 1},
                    {'title': 'Self-guided walk through Stone Town alleys', 'start_time': '15:00', 'duration_hours': 2, 'order': 2},
                    {'title': 'Forodhani Gardens night market street food', 'start_time': '18:30', 'duration_hours': 2, 'order': 3},
                ]
            },
            {
                'day_number': 2,
                'title': 'Stone Town history and spice tour',
                'description': 'Morning guided tour of Stone Town\'s historic sites. Afternoon spice farm tour in the countryside north of town.',
                'accommodation_notes': 'Same Stone Town hotel',
                'meals_notes': 'Breakfast at hotel, lunch included in spice tour',
                'activities': [
                    {'title': 'Guided Stone Town tour: Palace Museum, Slave Market, Old Fort', 'start_time': '09:00', 'duration_hours': 3, 'order': 1},
                    {'title': 'Spice farm tour with lunch', 'start_time': '14:00', 'duration_hours': 3, 'order': 2},
                    {'title': 'Sunset from the Palace roof terrace', 'start_time': '18:00', 'duration_hours': 1, 'order': 3},
                ]
            },
            {
                'day_number': 3,
                'title': 'Nungwi Beach',
                'description': 'Transfer to Nungwi on the northern tip of the island. Swimming, snorkelling, and relaxing on one of Zanzibar\'s best beaches.',
                'accommodation_notes': 'Nungwi beach hotel',
                'meals_notes': 'Breakfast, lunch and dinner at hotel',
                'activities': [
                    {'title': 'Transfer from Stone Town to Nungwi (1.5 hours)', 'start_time': '09:00', 'duration_hours': 1.5, 'order': 1},
                    {'title': 'Beach time and swimming', 'start_time': '11:00', 'duration_hours': 4, 'order': 2},
                    {'title': 'Sunset dhow cruise', 'start_time': '17:00', 'duration_hours': 2, 'estimated_cost_usd': 25, 'order': 3},
                ]
            },
            {
                'day_number': 4,
                'title': 'Snorkelling at Mnemba Atoll',
                'description': 'Day trip to Mnemba Atoll, a marine protected area off the northeast coast with excellent coral reef and marine life including sea turtles.',
                'accommodation_notes': 'Same Nungwi hotel',
                'meals_notes': 'Breakfast, packed lunch on boat',
                'activities': [
                    {'title': 'Boat trip to Mnemba Atoll', 'start_time': '08:30', 'duration_hours': 1, 'order': 1},
                    {'title': 'Snorkelling at Mnemba Atoll reef', 'duration_hours': 3, 'estimated_cost_usd': 40, 'order': 2},
                    {'title': 'Lunch on the boat', 'duration_hours': 1, 'order': 3},
                    {'title': 'Return to Nungwi, afternoon free on beach', 'duration_hours': 2, 'order': 4},
                ]
            },
            {
                'day_number': 5,
                'title': 'East coast and departure',
                'description': 'Morning drive to Paje on the east coast for a different beach experience before heading back to the airport.',
                'accommodation_notes': 'Checkout from Nungwi',
                'meals_notes': 'Breakfast at hotel',
                'activities': [
                    {'title': 'Drive to Paje beach via the east coast road', 'start_time': '09:00', 'duration_hours': 1.5, 'order': 1},
                    {'title': 'Paje beach walk and lunch', 'start_time': '10:30', 'duration_hours': 2, 'order': 2},
                    {'title': 'Transfer to Zanzibar Airport', 'start_time': '14:00', 'duration_hours': 1, 'order': 3},
                ]
            },
        ]
    },
    {
        'title': '10 Days Tanzania Complete: Safari + Kilimanjaro',
        'slug': '10-days-tanzania-complete-safari-kilimanjaro',
        'description': 'For those who want both the safari and the mountain in one trip. The itinerary does the safari first while your legs are fresh, then the Kilimanjaro climb.',
        'total_days': 10,
        'estimated_budget_usd': 5500,
        'difficulty_level': 'challenging',
        'days': [
            {
                'day_number': 1,
                'title': 'Arrive Arusha',
                'description': 'Arrive at Kilimanjaro International Airport. Transfer to Arusha. Rest and briefing.',
                'accommodation_notes': 'Arusha hotel',
                'meals_notes': 'Dinner on own',
                'activities': [
                    {'title': 'Airport transfer and hotel check-in', 'duration_hours': 2, 'order': 1},
                    {'title': 'Safari and climb briefing with guide', 'duration_hours': 1.5, 'order': 2},
                ]
            },
            {
                'day_number': 2,
                'title': 'Serengeti — arrive and first game drive',
                'description': 'Fly from Arusha to the Serengeti. Afternoon game drive after arrival.',
                'accommodation_notes': 'Tented camp in Serengeti',
                'meals_notes': 'Full board from lunch',
                'activities': [
                    {'title': 'Morning flight Arusha to Serengeti airstrip', 'start_time': '08:00', 'duration_hours': 1, 'estimated_cost_usd': 250, 'order': 1},
                    {'title': 'Afternoon game drive in Serengeti', 'start_time': '14:00', 'duration_hours': 4, 'order': 2},
                ]
            },
            {
                'day_number': 3,
                'title': 'Full day Serengeti',
                'description': 'Full day of game drives. Early morning is best for big cat activity.',
                'accommodation_notes': 'Same Serengeti camp',
                'meals_notes': 'Full board',
                'activities': [
                    {'title': 'Dawn game drive', 'start_time': '06:00', 'duration_hours': 4, 'order': 1},
                    {'title': 'Rest at camp, midday heat', 'start_time': '11:00', 'duration_hours': 3, 'order': 2},
                    {'title': 'Afternoon game drive to sunset', 'start_time': '15:30', 'duration_hours': 3, 'order': 3},
                ]
            },
            {
                'day_number': 4,
                'title': 'Ngorongoro Crater',
                'description': 'Morning flight or drive from Serengeti to Ngorongoro. Full day in the crater.',
                'accommodation_notes': 'Lodge on crater rim',
                'meals_notes': 'Full board, packed lunch in crater',
                'activities': [
                    {'title': 'Transfer to Ngorongoro', 'start_time': '07:00', 'duration_hours': 3, 'order': 1},
                    {'title': 'Crater descent and full day game drive', 'start_time': '11:00', 'duration_hours': 6, 'order': 2},
                    {'title': 'Crater ascent and dinner on rim', 'start_time': '17:00', 'duration_hours': 2, 'order': 3},
                ]
            },
            {
                'day_number': 5,
                'title': 'Drive to Moshi, Kilimanjaro preparation',
                'description': 'Drive from Ngorongoro to Moshi. Afternoon free to rest and prepare for the climb. Final gear check with your climbing guide.',
                'accommodation_notes': 'Moshi hotel',
                'meals_notes': 'Breakfast and dinner included',
                'activities': [
                    {'title': 'Drive from Ngorongoro to Moshi (4 hours)', 'start_time': '08:00', 'duration_hours': 4, 'order': 1},
                    {'title': 'Gear hire and final packing check', 'start_time': '15:00', 'duration_hours': 2, 'order': 2},
                ]
            },
            {
                'day_number': 6,
                'title': 'Kilimanjaro Day 1 — Machame Gate to Machame Camp',
                'description': 'Drive to Machame Gate and start the climb. Through the rainforest to Machame Camp.',
                'accommodation_notes': 'Machame Camp (2,835m)',
                'meals_notes': 'All meals at camp from lunch',
                'activities': [
                    {'title': 'Drive to Machame Gate', 'start_time': '08:00', 'duration_hours': 1.5, 'order': 1},
                    {'title': 'Registration and porter loading', 'start_time': '10:00', 'duration_hours': 1, 'order': 2},
                    {'title': 'Trek through rainforest to Machame Camp', 'start_time': '11:00', 'duration_hours': 5, 'order': 3},
                ]
            },
            {
                'day_number': 7,
                'title': 'Kilimanjaro Day 2 — Shira Plateau',
                'description': 'Climb from forest to moorland and onto the Shira Plateau. First views of the summit cone.',
                'accommodation_notes': 'Shira Camp (3,840m)',
                'meals_notes': 'All meals at camp',
                'activities': [
                    {'title': 'Trek to Shira Plateau', 'start_time': '08:00', 'duration_hours': 6, 'order': 1},
                ]
            },
            {
                'day_number': 8,
                'title': 'Kilimanjaro Day 3 — Lava Tower acclimatisation',
                'description': 'Acclimatisation day. Climb to Lava Tower at 4,600m then descend to Barranco Camp. Classic "climb high sleep low" profile.',
                'accommodation_notes': 'Barranco Camp (3,976m)',
                'meals_notes': 'All meals at camp',
                'activities': [
                    {'title': 'Trek to Lava Tower (4,600m)', 'start_time': '07:30', 'duration_hours': 4, 'order': 1},
                    {'title': 'Descend to Barranco Camp', 'start_time': '13:00', 'duration_hours': 2.5, 'order': 2},
                ]
            },
            {
                'day_number': 9,
                'title': 'Kilimanjaro Day 4 — Barranco Wall to Base Camp',
                'description': 'Climb the Barranco Wall in the morning, then continue to Barafu Base Camp. Early sleep before summit night.',
                'accommodation_notes': 'Barafu Camp (4,673m)',
                'meals_notes': 'All meals at camp, early dinner',
                'activities': [
                    {'title': 'Barranco Wall scramble', 'start_time': '07:30', 'duration_hours': 2, 'order': 1},
                    {'title': 'Continue to Barafu Base Camp', 'start_time': '10:00', 'duration_hours': 4, 'order': 2},
                    {'title': 'Rest and prepare summit gear, early sleep', 'start_time': '17:00', 'duration_hours': 2, 'order': 3},
                ]
            },
            {
                'day_number': 10,
                'title': 'Summit Night, Uhuru Peak, and descent to Moshi',
                'description': 'Midnight summit push to Uhuru Peak (5,895m) — the rooftop of Africa. Descend all the way back to Moshi by evening.',
                'accommodation_notes': 'Moshi hotel (celebration dinner)',
                'meals_notes': 'Summit snack, full meals at camp and hotel',
                'activities': [
                    {'title': 'Summit push from midnight to Uhuru Peak', 'start_time': '00:00', 'duration_hours': 7, 'order': 1},
                    {'title': 'Descend from summit to Mweka Camp', 'duration_hours': 5, 'order': 2},
                    {'title': 'Continue descent to Mweka Gate', 'duration_hours': 3, 'order': 3},
                    {'title': 'Transfer to Moshi, celebration dinner', 'duration_hours': 2, 'order': 4},
                ]
            },
        ]
    },
    {
        'title': '3 Days Arusha and Lake Manyara',
        'slug': '3-days-arusha-lake-manyara',
        'description': 'A short itinerary for those with limited time. Covers Arusha town and a full day game drive in Lake Manyara National Park.',
        'total_days': 3,
        'estimated_budget_usd': 600,
        'difficulty_level': 'easy',
        'days': [
            {
                'day_number': 1,
                'title': 'Arrive Arusha, explore the city',
                'description': 'Arrive in Arusha. Visit the Arusha National History Museum and the central market. Evening at leisure.',
                'accommodation_notes': 'Arusha town hotel',
                'meals_notes': 'Dinner on own account',
                'activities': [
                    {'title': 'Transfer from Kilimanjaro Airport to Arusha', 'duration_hours': 1, 'order': 1},
                    {'title': 'Arusha Natural History Museum visit', 'start_time': '14:00', 'duration_hours': 1.5, 'estimated_cost_usd': 5, 'order': 2},
                    {'title': 'Arusha central market walk', 'start_time': '16:00', 'duration_hours': 1, 'order': 3},
                ]
            },
            {
                'day_number': 2,
                'title': 'Lake Manyara National Park full day',
                'description': 'Full day game drive in Lake Manyara. The park is famous for tree-climbing lions, large elephant herds, flamingos, and hippos in the shallows.',
                'accommodation_notes': 'Return to Arusha hotel or stay near Manyara',
                'meals_notes': 'Packed lunch in the park',
                'activities': [
                    {'title': 'Drive from Arusha to Lake Manyara (2 hours)', 'start_time': '07:00', 'duration_hours': 2, 'order': 1},
                    {'title': 'Morning game drive in lake floor and forest zone', 'start_time': '09:30', 'duration_hours': 3, 'order': 2},
                    {'title': 'Picnic lunch by the lake', 'start_time': '12:30', 'duration_hours': 1, 'order': 3},
                    {'title': 'Afternoon game drive, focus on flamingo areas', 'start_time': '14:00', 'duration_hours': 3, 'order': 4},
                    {'title': 'Return drive to Arusha', 'start_time': '17:30', 'duration_hours': 2, 'order': 5},
                ]
            },
            {
                'day_number': 3,
                'title': 'Arusha coffee farm and departure',
                'description': 'Morning visit to a local coffee plantation on the slopes of Mount Meru. See how Tanzania\'s famous Arabica coffee is grown and processed before heading to the airport.',
                'accommodation_notes': 'Checkout from hotel',
                'meals_notes': 'Breakfast included',
                'activities': [
                    {'title': 'Coffee farm tour and tasting', 'start_time': '09:00', 'duration_hours': 2, 'estimated_cost_usd': 20, 'order': 1},
                    {'title': 'Transfer to Kilimanjaro Airport', 'start_time': '12:00', 'duration_hours': 1, 'order': 2},
                ]
            },
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed itineraries with days and activities'

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for itin_data in ITINERARIES:
            days_data = itin_data.pop('days')

            itinerary, is_new = Itinerary.objects.get_or_create(
                slug=itin_data['slug'],
                defaults={
                    'title': itin_data['title'],
                    'description': itin_data['description'],
                    'total_days': itin_data['total_days'],
                    'estimated_budget_usd': itin_data['estimated_budget_usd'],
                    'difficulty_level': itin_data['difficulty_level'],
                    'is_public': True,
                }
            )

            if not is_new:
                skipped += 1
                continue

            created += 1
            self.stdout.write(f'  Created: {itinerary.title}')

            for day_data in days_data:
                activities_data = day_data.pop('activities', [])

                day = ItineraryDay.objects.create(
                    itinerary=itinerary,
                    day_number=day_data['day_number'],
                    title=day_data['title'],
                    description=day_data.get('description', ''),
                    accommodation_notes=day_data.get('accommodation_notes', ''),
                    meals_notes=day_data.get('meals_notes', ''),
                )

                for act in activities_data:
                    ItineraryActivity.objects.create(
                        day=day,
                        title=act['title'],
                        description=act.get('description', ''),
                        start_time=act.get('start_time'),
                        duration_hours=act.get('duration_hours'),
                        estimated_cost_usd=act.get('estimated_cost_usd'),
                        order=act.get('order', 0),
                        notes=act.get('notes', ''),
                    )

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} itineraries created, {skipped} already existed.'
        ))
