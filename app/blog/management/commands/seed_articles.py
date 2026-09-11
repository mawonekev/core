from django.core.management.base import BaseCommand

from app.blog.models import Article

ARTICLES = [
    {
        'title': 'How to Climb Mount Kilimanjaro: A Beginner Guide',
        'slug': 'how-to-climb-mount-kilimanjaro-beginner-guide',
        'excerpt': 'Kilimanjaro is the highest peak in Africa and one of the most accessible high-altitude treks in the world. Here is everything you need to know before you go.',
        'content': """Mount Kilimanjaro stands at 5,895 metres above sea level and sits in northern Tanzania near the town of Moshi. It is a dormant volcano with three peaks — Kibo, Mawenzi, and Shira — and it draws thousands of climbers every year.

## Routes

There are seven official routes to the summit. The most popular ones are:

**Marangu Route** — The only route with hut accommodation. Often called the "Coca-Cola route". It is the shortest route at 5-6 days, which also means acclimatisation time is limited. Success rates are lower than longer routes.

**Machame Route** — The most popular route. Takes 6-7 days. Offers good acclimatisation with a "climb high, sleep low" profile. More scenic than Marangu.

**Lemosho Route** — Best for acclimatisation. 7-8 days. Starts on the quiet western side of the mountain and joins Machame route on the upper sections. Highest success rates.

## Best time to climb

The two best seasons are:
- **January to March** — dry, cold nights, usually clear skies
- **June to October** — the main dry season, busiest but reliable weather

Avoid April and May (long rains) and November (short rains).

## What to pack

The key is layers. You will go from tropical forest at the base to arctic conditions at the summit in just a few days.

- Moisture-wicking base layers
- Fleece mid-layer
- Waterproof jacket and trousers
- Insulated down jacket for summit night
- Warm gloves and balaclava
- Trekking poles (highly recommended)
- Headlamp with spare batteries

## Altitude sickness

Acute mountain sickness (AMS) is the biggest risk on Kilimanjaro. Symptoms include headache, nausea, and fatigue. The best prevention is choosing a longer route with more acclimatisation days, staying hydrated, and ascending slowly.

Diamox (acetazolamide) is commonly used as a preventive medication. Consult a doctor before the climb.

## Cost

Budget for USD 2,000 to 4,500 depending on the route, number of days, and operator. This typically includes park fees, guides, porters, accommodation, and meals on the mountain.

Park fees alone are around USD 900-1,000 for a 7-day climb.

## Tips

- Book with a reputable operator who treats porters fairly
- Pole pole (slowly slowly) — do not rush the ascent
- Drink 3-4 litres of water per day on the mountain
- Summit night starts around midnight — be mentally prepared
""",
        'status': 'published',
        'is_approved': True,
    },
    {
        'title': 'Serengeti National Park: When to Go and What to Expect',
        'slug': 'serengeti-national-park-when-to-go-what-to-expect',
        'excerpt': 'The Serengeti is home to one of the greatest wildlife spectacles on earth. This guide covers the wildebeest migration, best game viewing seasons, and practical tips for your safari.',
        'content': """The Serengeti National Park covers 14,763 square kilometres of open savanna in northern Tanzania. It is one of the oldest ecosystems on the planet and one of the best places in Africa to see wildlife.

## The Great Migration

Every year, more than 1.5 million wildebeest and hundreds of thousands of zebras and gazelles move in a continuous circle across the Serengeti and into Kenya's Masai Mara in search of fresh grass and water. This is the Great Migration, and it is the primary reason most people visit.

The migration does not stop — the herds are always moving. Where you find them depends on when you visit:

- **January to March** — Herds are in the southern Serengeti (Ndutu area). Calving season, with up to 500,000 calves born in a few weeks. Predator activity is high.
- **April to May** — Moving northwest through the central Serengeti. Long grass, fewer tourists.
- **June to July** — Reaching the Western Corridor near the Grumeti River. Crocodile crossings begin.
- **July to October** — Northern Serengeti and Masai Mara. The famous Mara River crossings happen here — dramatic scenes of thousands of wildebeest plunging into crocodile-filled water.
- **November to December** — Herds move back south through the eastern Serengeti.

## Beyond the migration

The Serengeti has year-round wildlife. Large resident lion prides, leopards, cheetahs, elephants, buffalo, and over 500 bird species live here regardless of season.

## Getting there

The main entry point is Seronera in the central Serengeti. Most visitors fly into Kilimanjaro International Airport or Julius Nyerere International Airport in Dar es Salaam, then connect to one of the airstrips inside the park.

## Where to stay

There are three accommodation tiers inside the Serengeti:
- **Budget**: Public campsites (basic facilities, bring your own gear)
- **Mid-range**: Permanent tented camps with en-suite facilities
- **Luxury**: Private conservancy lodges with exclusive game drives

Staying inside the park allows early morning and late evening game drives when animals are most active.

## Tips

- Bring binoculars — the plains are vast
- A good zoom lens (400mm+) makes a big difference for wildlife photography
- Book accommodation and park fees in advance, especially for peak season (July to October)
- The Serengeti does not allow walking outside of designated areas
""",
        'status': 'published',
        'is_approved': True,
    },
    {
        'title': 'Zanzibar Travel Guide: Beaches, Stone Town, and Spice Tours',
        'slug': 'zanzibar-travel-guide-beaches-stone-town-spice-tours',
        'excerpt': 'Zanzibar is an island off the coast of Tanzania famous for white sand beaches, crystal clear water, and the historic Stone Town. Here is how to make the most of your trip.',
        'content': """Zanzibar (officially Unguja) is a semi-autonomous island about 35 kilometres off the Tanzanian coast. It has a distinct culture shaped by African, Arab, Indian, and Portuguese influences, and a history tied to the spice trade and, painfully, to the East African slave trade.

## Stone Town

Stone Town is a UNESCO World Heritage Site and the historic centre of Zanzibar City. The narrow winding streets, carved wooden doors, mosques, and old trading houses reflect centuries of Swahili, Omani, and colonial history.

Key things to see in Stone Town:
- **The House of Wonders** — the largest building in Stone Town, once a palace
- **The Old Fort** — built by the Omanis in the 17th century
- **The Slave Market Memorial** — a sobering but important part of the island's history
- **Darajani Market** — the central market, busy every morning
- **Forodhani Gardens** — seafront promenade with street food stalls that come alive at night

## Beaches

The beaches vary depending on which side of the island you visit:

- **North (Nungwi and Kendwa)** — wide white sand beaches with calm water. Best for swimming any time of day as the tide does not go out as far.
- **East (Paje, Jambiani)** — long beaches with turquoise water. Popular for kitesurfing. The tide goes very far out at low tide, which limits swimming windows.
- **Southeast (Bwejuu)** — quieter, fewer tourists, beautiful at high tide.

## Spice tours

Zanzibar was once the world's leading producer of cloves. Spice tours take you to farms where you can see and smell nutmeg, vanilla, cinnamon, black pepper, turmeric, and cardamom growing. Guides peel, crush, and taste each spice. Most tours last half a day and cost around USD 15-25.

## Getting around

Zanzibar has dala-dalas (shared minibuses) that connect Stone Town to most parts of the island cheaply. Taxis and motorbike taxis (piki-piki) are widely available. Renting a scooter gives you the most flexibility.

## Best time to visit

The best time is June to October (dry season). Avoid April and May (heavy rains). March is also quite rainy. January and February are warm and mostly dry.

## Tips

- Dress modestly in Stone Town — Zanzibar is predominantly Muslim
- Bargaining is expected in markets
- Friday afternoons many businesses close for prayers
- Water visibility for snorkelling is best from October to February
""",
        'status': 'published',
        'is_approved': True,
    },
    {
        'title': 'Ngorongoro Crater: The Complete Visitor Guide',
        'slug': 'ngorongoro-crater-complete-visitor-guide',
        'excerpt': 'The Ngorongoro Crater is a natural wonder — a volcanic caldera that shelters one of the densest concentrations of wildlife in Africa, including the endangered black rhino.',
        'content': """The Ngorongoro Crater is the world's largest intact volcanic caldera and one of Tanzania's most visited attractions. It sits at around 2,300 metres elevation and covers 260 square kilometres. The crater floor hosts roughly 25,000 large animals in a relatively small space, making game viewing exceptionally productive.

## Wildlife in the crater

The crater has a self-contained ecosystem with permanent water sources, which means animals do not need to migrate out. You can expect to see:

- **Lions** — one of the highest densities of lions in Africa. The inbred Crater lions are recognizable by the males' dark manes.
- **Black rhino** — Ngorongoro is one of the last places in Tanzania where black rhino can be reliably spotted. Numbers are small (around 20-30) but sightings happen regularly.
- **Elephant** — mostly older bull elephants in the crater. Females and young are more common on the crater rim.
- **Hippo** — found in the hippo pool near the Munge River.
- **Flamingo** — Lake Magadi in the crater floor hosts flamingo flocks.
- **Hyena** — very common. The crater has large hyena clans.

## Getting there

Ngorongoro is about 180 kilometres west of Arusha on a good tarmac road (roughly 3 hours drive). The crater rim is at 2,300 metres, and the descent to the floor takes about 20 minutes on a steep dirt road.

## Park fees and rules

The crater charges separate fees from the Ngorongoro Conservation Area. As of 2024, a full-day crater fee is USD 295 per vehicle (not per person). These fees are on top of the Conservation Area entrance fee.

You are not allowed to exit your vehicle inside the crater except at designated picnic spots. Walking on the crater floor is prohibited.

## When to visit

Game viewing is good year-round because wildlife does not migrate out. July to October is drier and easier to drive. Wet season (March to May) turns the roads muddy but the crater is lush and green.

Morning game drives (6am start) are best as most predators are active and the light is good.

## Combining with Serengeti

Most itineraries combine Ngorongoro with the Serengeti. They are adjacent — you can drive between them in under two hours. A typical Northern Tanzania circuit: Arusha → Tarangire → Ngorongoro → Serengeti → return.

## Tips

- Bring warm clothes — the rim is cold early in the morning
- Carry your own food and drinks into the crater (there are no shops inside)
- Allocate a full day for the crater, not a half day
- Book in advance, especially for the descent permits during peak season
""",
        'status': 'published',
        'is_approved': True,
    },
    {
        'title': 'Tanzania Safari Budget Guide: How Much Does it Actually Cost?',
        'slug': 'tanzania-safari-budget-guide-how-much-does-it-cost',
        'excerpt': 'Tanzania safaris have a reputation for being expensive, and they can be. But there is a range. This guide breaks down what you will actually pay at every budget level.',
        'content': """Tanzania is not a cheap safari destination. High park fees, mandatory game drive vehicles, and the cost of accommodation inside national parks add up quickly. But the range is wide — from a shoestring camping trip to a USD 2,000-per-night luxury tented lodge.

## Why Tanzania safaris are expensive

The main cost drivers:
1. **Park fees** — Tanzania charges per-person, per-day fees in most parks. Serengeti is USD 70 per person per day. Ngorongoro crater adds an extra USD 295 per vehicle per descent. These fees are non-negotiable.
2. **4WD vehicle** — You need a safari vehicle. Most operators charge per vehicle, not per person, so solo travellers pay more.
3. **Accommodation** — Budget options exist but even midrange tented camps start at USD 150-300 per person per night inside the parks.

## Budget breakdown by tier

### Budget (USD 100-200/day per person)
Camping in public campsites, shared group safari vehicles, simple meals. You will cover park fees and basic accommodation. Possible but requires planning and some comfort sacrifice.

- Use the Northern Circuit (Serengeti, Ngorongoro, Tarangire) on a 6-8 day group safari
- Book with a budget operator in Arusha
- Expect to share a vehicle with 5-7 others
- Campsites provide basic toilets and water

### Mid-range (USD 250-500/day per person)
Permanent tented camps or budget lodges, private or semi-private vehicle, full board.

- Comfortable canvas tents with proper beds and en-suite bathrooms
- More flexibility on game drive timing
- Smaller groups

### Luxury (USD 600-2,000+/day per person)
Private lodges and exclusive-use camps, private vehicle and guide, premium food and service.

- Some properties are inside private concessions where walking safaris are allowed
- Exclusive game drives — no other vehicles at sightings
- Fly-in options eliminate long road drives between parks

## Sample itinerary costs

**7-day Northern Circuit (budget group)**: USD 2,000-3,000 per person total
Covers: park fees, shared 4WD, camping or budget lodges, all meals on safari

**7-day Northern Circuit (mid-range)**: USD 3,500-5,000 per person total
Covers: park fees, private vehicle, tented camps, all meals

**5-day Serengeti only (luxury fly-in)**: USD 5,000-10,000+ per person total
Covers: park fees, flights, exclusive lodge, private guide

## Where to save money

- Travel in low season (April, May, November) — some lodges drop prices by 30-50%
- Book last-minute with Arusha-based operators for group safaris
- Combine parks efficiently — multiple parks in one loop saves on driving days
- Zanzibar after the safari is a natural add-on and relatively affordable

## Kilimanjaro vs safari cost

A 7-day Kilimanjaro climb typically costs USD 2,000-4,000 per person. That is comparable to a mid-range safari. If you are doing both, budget USD 5,000-8,000 for a two-week Tanzania trip at mid-range level.
""",
        'status': 'published',
        'is_approved': True,
    },
    {
        'title': 'Tarangire National Park: The Hidden Gem of Northern Tanzania',
        'slug': 'tarangire-national-park-hidden-gem-northern-tanzania',
        'excerpt': 'Tarangire is often skipped in favour of the Serengeti and Ngorongoro but it deserves its own dedicated visit. Famous for huge elephant herds, ancient baobab trees, and excellent dry-season game viewing.',
        'content': """Tarangire National Park sits about 120 kilometres south of Arusha. It covers 2,850 square kilometres and is defined by the Tarangire River, which becomes the main water source for thousands of animals during the dry season.

## Why visit Tarangire

Most itineraries skip Tarangire or include it as a single-day stop on the way to the Serengeti. That is a mistake. Tarangire has a distinctive character:

**Elephants** — Tarangire has one of the highest elephant densities in Tanzania. During the dry season (June to October), hundreds of elephants gather along the river. It is not unusual to see herds of 50-100.

**Baobab trees** — The landscape is dominated by ancient baobab trees, some thousands of years old. They give Tarangire a unique atmosphere unlike any other Tanzanian park.

**Bird diversity** — Over 550 bird species have been recorded in Tarangire, making it exceptional for birding. The dry woodland and wetlands attract everything from ostriches to yellow-collared lovebirds.

**Fewer tourists** — Tarangire gets a fraction of the visitors that Serengeti and Ngorongoro receive, which means quieter game drives and more space.

## Dry season vs wet season

**Dry season (June to October)** is the best time. The Tarangire River is the only water source, so animals concentrate along it. Game viewing density is exceptional.

**Wet season (November to May)** — Animals disperse across the ecosystem, making them harder to find. But the park is green, migratory birds arrive, and wildebeest and zebra move in to give birth.

## What else to see

- **Silale Swamp** — hippos, buffalo, and waterbirds
- **Lemiyon area** — good for tree-climbing lions (yes, some Tarangire lions have learned this)
- **Kwa Kuchinja corridor** — a wildlife migration corridor connecting Tarangire to Lake Manyara

## Getting there

About 2 hours from Arusha on tarmac road. Most visitors combine Tarangire with Lake Manyara, Ngorongoro, and Serengeti on the Northern Circuit.

## Tips

- Visit in September or October for peak elephant concentrations
- Tarangire is excellent for a night drive (check if your operator offers it — not all parks allow it)
- Stay at least 2 days to explore different areas of the park
""",
        'status': 'published',
        'is_approved': True,
    },
]


class Command(BaseCommand):
    help = 'Seed blog articles with Tanzania travel content'

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for data in ARTICLES:
            article, is_new = Article.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'excerpt': data['excerpt'],
                    'content': data['content'],
                    'status': data['status'],
                    'is_approved': data['is_approved'],
                    'is_published': True,
                }
            )
            if is_new:
                created += 1
                self.stdout.write(f'  Created: {article.title}')
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} articles created, {skipped} already existed.'
        ))
