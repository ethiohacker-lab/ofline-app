"""
Pre-seeded academic & conversational knowledge base for Maya.
Covers Everyday English (greetings, common words, grammar, writing, idioms),
Ethiopian greetings, Ethiopian University Horticulture curriculum,
and Computer Science curriculum.
"""

from __future__ import annotations

from typing import Dict, List


SEED_KNOWLEDGE: List[Dict[str, str]] = [
    # =========================================================================
    # GENERAL, MAYA IDENTITY & ETHIOPIAN CONVERSATIONAL
    # =========================================================================
    {
        "question": "Who is Maya what can Maya do introduce yourself",
        "answer": (
            "I am **Maya**, your offline-first, self-learning AI assistant! "
            "I run right on your phone without cloud LLMs or neural networks:\n"
            "1) **Everyday English & Conversation:** Greetings, common words, grammar, and offline `summarize: <text>`.\n"
            "2) **Deterministic Math & Domain Calculators:** Equations, matrices, statistics, `timad`/`quintal` conversions, Horticulture dosages, and IPv4 subnetting.\n"
            "3) **Hybrid Offline Brain + Online Sync:** I learn from every fact you teach me—and when connected, I can fetch Wikipedia & Dictionary knowledge into SQLite for future offline use!"
        ),
        "category": "General",
        "tags": "maya who are you capabilities self introduction offline brain",
    },
    {
        "question": "Selam hello hi good morning good afternoon ethiopian greeting",
        "answer": (
            "Selam! Hello and welcome to **Maya**. "
            "Ask me about everyday English, Mathematics, Horticulture, or Computer Science—or teach me new facts anytime!"
        ),
        "category": "General",
        "tags": "selam greeting hello hi hey good morning ethiopia maya",
    },
    {
        "question": "What are common Amharic Ethiopian greetings and their meanings?",
        "answer": (
            "Essential Ethiopian (Amharic) greetings:\n"
            "• **Selam (ሰላም):** Peace / Hello (universal greeting).\n"
            "• **Endemin neh / Endemin nesh?** How are you? (to male / female).\n"
            "• **Egziabher yimesgen, dehna negn:** Thanks to God, I am well.\n"
            "• **Endemin aderk / adersh?** Good morning (How did you spend the night?).\n"
            "• **Endemin walk / walsh?** Good afternoon (How did you spend the day?).\n"
            "• **Ameseginalehu (አመሰግናለሁ):** Thank you.\n"
            "• **Dehna hun / huni (Chaw):** Goodbye / Stay well."
        ),
        "category": "General",
        "tags": "amharic ethiopian greetings selam endemin neh ameseginalehu tena yistilign",
    },
    {
        "question": "What are effective study tips for university exams active recall spaced repetition",
        "answer": (
            "Top evidence-based study strategies:\n"
            "• **Active Recall:** Close your notes and test yourself (try typing `quiz me` here with Maya!).\n"
            "• **Spaced Repetition:** Review material after 1 day, 3 days, 7 days, and 21 days.\n"
            "• **Pomodoro Technique:** Focus deeply for 25–50 minutes, then rest 5–10 minutes.\n"
            "• **Feynman Method:** Explain a topic simply—try teaching Maya new Horticulture or CS concepts!"
        ),
        "category": "General",
        "tags": "study tips exam preparation pomodoro spaced repetition active recall",
    },

    # =========================================================================
    # EVERYDAY ENGLISH: COMMON PHRASES, GRAMMAR, VOCABULARY & WRITING
    # =========================================================================
    {
        "question": "What are common everyday English greetings and polite expressions?",
        "answer": (
            "Common English greetings & polite phrases:\n"
            "• **Greetings:** *Hello*, *Hi there*, *Good morning*, *Good afternoon*, *Good evening*, *How are you doing?*, *Nice to meet you.*\n"
            "• **Replies:** *I'm doing well, thank you!*, *Pretty good, how about you?*, *It's a pleasure to meet you.*\n"
            "• **Polite Requests:** *Could you please help me?*, *Excuse me*, *Pardon me*, *I really appreciate it.*\n"
            "• **Farewells:** *Goodbye*, *See you soon*, *Take care*, *Have a great day!*"
        ),
        "category": "English",
        "tags": "english greetings polite phrases hello good morning how are you thank you goodbye",
    },
    {
        "question": "What are the most common English conversational sentences for daily life?",
        "answer": (
            "Useful everyday English sentences:\n"
            "• **Asking for help:** *\"Could you explain that again, please?\"* / *\"Can you give me an example?\"*\n"
            "• **Checking understanding:** *\"Do you see what I mean?\"* / *\"Does that make sense?\"*\n"
            "• **Expressing opinion:** *\"In my opinion…\"* / *\"From my perspective…\"* / *\"I agree with that point.\"*\n"
            "• **Polite disagreement:** *\"I see your point, however…\"* / *\"That's interesting, though I think…\"*\n"
            "• **Clarifying:** *\"In other words…\"* / *\"What I meant to say is…\"*"
        ),
        "category": "English",
        "tags": "english common sentences daily conversation speaking phrases",
    },
    {
        "question": "Explain the 8 parts of speech in English grammar with examples",
        "answer": (
            "The 8 Parts of Speech in English:\n"
            "1) **Noun:** Names a person, place, thing, or idea (*coffee, Ethiopia, algorithm*).\n"
            "2) **Pronoun:** Replaces a noun (*she, they, it, which*).\n"
            "3) **Verb:** Expresses action or state (*grow, compute, is, learn*).\n"
            "4) **Adjective:** Describes a noun (*fertile soil, fast algorithm*).\n"
            "5) **Adverb:** Modifies a verb, adjective, or adverb (*quickly, very, carefully*).\n"
            "6) **Preposition:** Shows relationship in time/space (*in, on, under, between*).\n"
            "7) **Conjunction:** Connects words or clauses (*and, but, because, although*).\n"
            "8) **Interjection:** Expresses sudden emotion (*Wow!, Hey!, Oh!*)."
        ),
        "category": "English",
        "tags": "english grammar parts of speech noun verb adjective adverb preposition conjunction",
    },
    {
        "question": "Explain English verb tenses present past and future simply",
        "answer": (
            "Core English Tenses:\n"
            "• **Simple Present:** Habit or general truth (*\"Water boils at 100°C.\" / \"She studies CS.\"*)\n"
            "• **Present Continuous:** Happening right now (*\"I am learning offline with Maya.\"*)\n"
            "• **Present Perfect:** Past action connected to now (*\"I have finished my lab report.\"*)\n"
            "• **Simple Past:** Completed past event (*\"We planted seedlings yesterday.\"*)\n"
            "• **Future (`will` / `going to`):** Planned or predicted action (*\"I will review SQL tonight.\"*)"
        ),
        "category": "English",
        "tags": "english verb tenses grammar present past future continuous perfect",
    },
    {
        "question": "What is the difference between active voice and passive voice in English?",
        "answer": (
            "• **Active Voice** (`Subject + Verb + Object`): The subject performs the action. Direct, clear, and preferred in most writing.\n"
            "  *Example:* *\"The agronomist measured soil pH.\"*\n"
            "• **Passive Voice** (`Object + be + Past Participle + by Subject`): Emphasizes the action or result rather than who did it—common in scientific methods sections.\n"
            "  *Example:* *\"Soil pH was measured by the agronomist.\"*"
        ),
        "category": "English",
        "tags": "active passive voice english grammar scientific writing",
    },
    {
        "question": "Explain commonly confused English words affect vs effect their vs there its vs it's",
        "answer": (
            "Commonly Confused English Words:\n"
            "• **Affect (verb)** = to influence (*\"Shade affects coffee yield.\"*); **Effect (noun)** = the result (*\"The effect was positive.\"*).\n"
            "• **Their** = belonging to them; **There** = place/existence; **They're** = they are.\n"
            "• **Its** = possessive (*\"The tree lost its leaves.\"*); **It's** = *it is* or *it has*.\n"
            "• **Your** = possessive; **You're** = *you are*.\n"
            "• **Accept** = receive/agree; **Except** = excluding."
        ),
        "category": "English",
        "tags": "affect effect their there they're its it's confused english words spelling",
    },
    {
        "question": "How do you write a clear academic paragraph or essay PEEL structure?",
        "answer": (
            "Use the **PEEL** structure for crisp academic & technical writing:\n"
            "• **P — Point:** Open with a clear topic sentence stating your main claim.\n"
            "• **E — Evidence:** Support it with data, citations, or concrete examples.\n"
            "• **E — Explanation:** Analyze *why* or *how* the evidence proves your point.\n"
            "• **L — Link:** Connect back to your thesis or smoothly transition to the next paragraph."
        ),
        "category": "English",
        "tags": "essay writing academic paragraph peel structure topic sentence",
    },
    {
        "question": "What are common English transition words for essays and reports?",
        "answer": (
            "High-impact English transition words:\n"
            "• **Adding ideas:** *Furthermore, Moreover, In addition, Additionally.*\n"
            "• **Contrasting:** *However, Nevertheless, On the other hand, Conversely, Although.*\n"
            "• **Cause & Effect:** *Therefore, Consequently, As a result, Because of this, Thus.*\n"
            "• **Examples:** *For instance, Specifically, Such as, Namely.*\n"
            "• **Concluding:** *In conclusion, Ultimately, Overall, To summarize.*"
        ),
        "category": "English",
        "tags": "transition words linking words english essay writing furthermore however therefore",
    },
    {
        "question": "What are common English idioms and their meanings?",
        "answer": (
            "Popular everyday English idioms:\n"
            "• **Break a leg:** Good luck!\n"
            "• **Hit the books:** Study seriously.\n"
            "• **Piece of cake:** Very easy to do.\n"
            "• **Under the weather:** Feeling slightly sick or tired.\n"
            "• **Think outside the box:** Find a creative, original solution.\n"
            "• **Once in a blue moon:** Very rarely."
        ),
        "category": "English",
        "tags": "english idioms phrases meanings hit the books piece of cake",
    },

    # =========================================================================
    # HORTICULTURE: COFFEE, TEA & SPICES PRODUCTION (ETHIOPIAN CURRICULUM)
    # =========================================================================
    {
        "question": "What are the optimal growing conditions for Arabica coffee in Ethiopia?",
        "answer": (
            "Coffea arabica (indigenous to Ethiopian highlands like Kaffa, Sidama, Yirgacheffe, Jimma, and Harar) thrives under:\n"
            "• Altitude: 1,500–2,100 m a.s.l. (specialty profiles often 1,750–2,100 m)\n"
            "• Temperature: 18–22°C ideal mean; frost-free\n"
            "• Rainfall: 1,400–2,000 mm/year well distributed, with a 2–3 month dry period to trigger uniform flowering\n"
            "• Soil: Deep, well-drained volcanic loam/Nitisols rich in organic matter, pH 5.2–6.2."
        ),
        "category": "Horticulture",
        "tags": "arabica coffee coffea altitude rainfall soil ph ethiopia agronomy",
    },
    {
        "question": "Why is shade management important in coffee production and which shade trees are used?",
        "answer": (
            "Shade management regulates microclimate (reduces leaf temperature by 2–4°C), prevents biennial bearing/overbearing dieback, reduces weed pressure, recycles organic matter, and improves cup acidity and bean density. "
            "Recommended multi-purpose leguminous/native shade trees in Ethiopia include Albizia gummifera, Millettia ferruginea (Birbira), Cordia africana (Wanza), Sesbania sesban, and Erythrina abyssinica—typically managed for 30–50% filtered canopy cover."
        ),
        "category": "Horticulture",
        "tags": "coffee shade management trees albizia cordia birbira microclimate",
    },
    {
        "question": "Compare wet washed coffee processing vs dry natural coffee processing",
        "answer": (
            "• Wet (Washed) Processing: Ripe red cherries are pulped within 12–24 hours, fermented (12–48 hours depending on temperature) to break down mucilage, washed in channels, and dried on raised beds to 10.5–11.5% moisture. Produces clean, bright, floral/citrus acidity (e.g., Washed Yirgacheffe).\n"
            "• Dry (Natural) Processing: Whole ripe cherries are sun-dried on raised mesh beds for 15–21 days with frequent turning to prevent mold/ochratoxin, then hulled. Produces heavy body, sweet berry/winey notes (e.g., Natural Guji/Harar)."
        ),
        "category": "Horticulture",
        "tags": "wet washed dry natural coffee processing fermentation raised beds",
    },
    {
        "question": "How does Ethiopian coffee quality grading work?",
        "answer": (
            "Ethiopian green coffee is graded by the ECX / Ethiopian Coffee and Tea Authority using:\n"
            "1) Green bean physical inspection (300 g sample): counting primary defects (full black, sour, fungus) and secondary defects (broken, insect-damaged, hulls), plus screen size and moisture (<=11.5%).\n"
            "2) Cupping evaluation (Specialty Q-grading scale out of 100): fragrance/aroma, flavor, aftertaste, acidity, body, balance, uniformity, clean cup, sweetness. Grade 1 & Grade 2 are top specialty grades (85+ points)."
        ),
        "category": "Horticulture",
        "tags": "coffee quality grading ecx defects cupping specialty grade 1 2",
    },
    {
        "question": "How is Korarima Ethiopian cardamom cultivated and cured?",
        "answer": (
            "Korarima (Aframomum corrorima) is a native perennial shade-loving spice crop of southwestern Ethiopia (Kaffa, Bench-Sheko, Gambella).\n"
            "• Ecology: Humid forest understory (1,350–2,000 m), 1,500–2,000 mm rainfall, 50–65% shade.\n"
            "• Propagation: Division of healthy rhizomes or seed.\n"
            "• Harvesting & Curing: Harvest mature red capsules at 2–3 years; dry gently in shade or solar dryers (avoid direct smoke curing which lowers essential oil quality) down to ~10% moisture."
        ),
        "category": "Horticulture",
        "tags": "korarima ethiopian cardamom spice aframomum rhizome curing",
    },
    {
        "question": "What are the agronomy and curing practices for ginger and turmeric?",
        "answer": (
            "• Ginger (Zingiber officinale) & Turmeric (Curcuma longa): Warm humid lowlands to mid-altitudes (1,000–1,800 m), well-drained sandy loam, propagated via disease-free seed rhizomes (25–40 g with 2–3 buds) planted at 30 × 15–20 cm.\n"
            "• Mulching immediately after planting conserves moisture and suppresses weeds.\n"
            "• Turmeric Curing: Boil harvested rhizomes in water for 45–60 minutes until soft to gelatinize starch and distribute curcumin pigment evenly, then sun-dry for 10–15 days and polish."
        ),
        "category": "Horticulture",
        "tags": "ginger turmeric spice rhizome boiling curing mulch",
    },
    {
        "question": "What are the processing steps of black tea vs green tea?",
        "answer": (
            "Both come from Camellia sinensis (harvested as 'two leaves and a bud'):\n"
            "• Black Tea (Orthodox or CTC): Withering (12–18 h to reduce moisture) → Rolling/CTC maceration (ruptures cells) → Oxidation/Fermentation (polyphenol oxidase converts catechins to theaflavins & thearubigins) → Firing/Drying (90–100°C) → Grading.\n"
            "• Green Tea: Immediately steamed or pan-fired after plucking to denature polyphenol oxidase enzymes and prevent oxidation, followed by rolling and drying."
        ),
        "category": "Horticulture",
        "tags": "tea processing camellia sinensis black green ctc oxidation withering",
    },

    # =========================================================================
    # HORTICULTURE: CROP PRODUCTION, FRUITS, VEGETABLES & PROTECTION
    # =========================================================================
    {
        "question": "Explain Enset false banana propagation and kocho processing",
        "answer": (
            "Enset (Ensete ventricosum) is Ethiopia's drought-resilient root/stem food security crop.\n"
            "• Propagation: Macro-propagation from corm ('mother corm')—the central apical meristem is scooped out and packed with soil/manure to break apical dominance, producing 40–100 suckers per corm.\n"
            "• Processing: Leaf sheaths are decorticated (scraped) with bamboo scrapers and mixed with pulverized corm, then fermented anaerobically in leaf-lined pits for weeks to months to produce Kocho, while pressed liquid settles into fine starch called Bulla."
        ),
        "category": "Horticulture",
        "tags": "enset false banana corm suckers kocho bulla ethiopia propagation",
    },
    {
        "question": "What are best practices for onion and tomato production in Ethiopia?",
        "answer": (
            "• Onion (Allium cepa, e.g., Bombay Red, Adama Red): Raise seedlings in sunken/raised nursery beds for 45–55 days; transplant on double-row ridges (20 cm between rows × 10 cm between plants). Stop irrigation 10–14 days before harvest when 70% of tops fall over, then cure bulbs.\n"
            "• Tomato (Solanum lycopersicum): Transplant at 70–100 × 30–40 cm, stake indeterminate varieties, avoid overhead irrigation late in the day to limit Late Blight, and apply balanced NPK + Calcium to prevent blossom-end rot."
        ),
        "category": "Horticulture",
        "tags": "onion tomato vegetable production spacing nursery curing blossom end rot",
    },
    {
        "question": "How are tropical and subtropical fruits like mango avocado and banana managed?",
        "answer": (
            "• Mango & Avocado: Propagate superior cultivars via cleft/veneer grafting onto vigorous local rootstocks (avoids 7–10 year juvenile phase of seedlings and ensures true-to-type fruit). Space 8–10 m; prune for open canopy.\n"
            "• Banana: Propagate using sword suckers or tissue-culture plantlets to prevent Banana Bunchy Top / Panama disease; maintain a 3-generation mat (mother, daughter, grand-daughter) by desuckering excess shoots."
        ),
        "category": "Horticulture",
        "tags": "mango avocado banana fruit orchard grafting sucker pruning",
    },
    {
        "question": "What is Integrated Pest Management IPM and its core steps?",
        "answer": (
            "Integrated Pest Management (IPM) is an ecosystem-based strategy that keeps pest populations below the Economic Injury Level (EIL) while minimizing chemical hazards:\n"
            "1) Prevention & Cultural Control (crop rotation, resistant varieties, field sanitation, proper spacing)\n"
            "2) Regular Monitoring & Scouting (action thresholds)\n"
            "3) Mechanical & Physical Control (handpicking, traps, mulching)\n"
            "4) Biological Control (predators like ladybird beetles, parasitoids, Trichoderma)\n"
            "5) Selective Chemical Control only as a last resort, rotating modes of action to prevent resistance."
        ),
        "category": "Horticulture",
        "tags": "ipm integrated pest management threshold biological cultural control",
    },
    {
        "question": "How do you identify and manage Coffee Berry Disease CBD and Coffee Wilt Disease?",
        "answer": (
            "• Coffee Berry Disease (CBD, Colletotrichum kahawae): Fungal disease causing dark sunken necrotic lesions on green berries, leading to premature berry drop or mummified cherries at high altitudes (>1,700 m). Manage with CBD-resistant Ethiopian selections (e.g., 741, 7440, 74110), pruning to lower humidity, and timely copper-based sprays.\n"
            "• Coffee Wilt Disease (CWD / Tracheomycosis, Fusarium xylarioides): Vascular wilt causing yellowing, defoliation, and blue-black streaks beneath the bark. Manage strictly by uprooting and burning infected trees on-site, disinfecting tools, and planting resistant varieties."
        ),
        "category": "Horticulture",
        "tags": "coffee berry disease cbd wilt cwd pathology colletotrichum fusarium",
    },
    {
        "question": "What causes Late Blight in potato and tomato and how is it controlled?",
        "answer": (
            "Late Blight is caused by the oomycete Phytophthora infestans (favored by cool, humid, rainy weather 15–22°C). Symptoms include water-soaked dark lesions on leaves with white cottony sporulation underneath, rapidly collapsing foliage and rotting tubers.\n"
            "Control: Plant certified disease-free seed tubers and resistant cultivars (e.g., Gudenie, Belete), hill soil deeply over potato tubers, destroy volunteer plants/cull piles, and alternate protectant (Mancozeb) and systemic fungicides before severe outbreak."
        ),
        "category": "Horticulture",
        "tags": "late blight potato tomato phytophthora infestans fungicide pathology",
    },
    {
        "question": "Explain weed management and the critical period of weed competition",
        "answer": (
            "The Critical Period of Weed Competition (CPWC) is the specific growth window during which weeds must be controlled to prevent irreversible yield loss (typically the first 25–40% of a crop's life cycle, e.g., 2–6 weeks after transplanting vegetables).\n"
            "Integrated Weed Management combines stale seedbed preparation, dense/timely planting, organic or plastic mulching, inter-row hoeing, crop rotation (to break parasitic weeds like Striga hermonthica or Orobanche), and targeted herbicides."
        ),
        "category": "Horticulture",
        "tags": "weed management critical period cpwc striga mulching",
    },

    # =========================================================================
    # HORTICULTURE: SOIL, IRRIGATION, PROPAGATION & POSTHARVEST
    # =========================================================================
    {
        "question": "Explain NPK soil fertility and nitrogen phosphorus potassium functions in plants",
        "answer": (
            "• Nitrogen (N): Drives vegetative leaf/stem growth and chlorophyll synthesis; deficiency shows uniform yellowing (chlorosis) starting on older lower leaves.\n"
            "• Phosphorus (P): Essential for ATP energy transfer, root development, flowering, and seed set; deficiency causes stunted growth and purplish tint on older leaves.\n"
            "• Potassium (K): Regulates stomatal opening, osmotic balance, sugar transport, and fruit quality/disease resistance; deficiency causes scorching/necrosis along older leaf margins."
        ),
        "category": "Horticulture",
        "tags": "npk nitrogen phosphorus potassium soil fertility deficiency symptoms",
    },
    {
        "question": "What are effective soil and water conservation practices in highland agriculture?",
        "answer": (
            "Soil and water conservation (SWC) prevents erosion and boosts infiltration on sloped farms:\n"
            "• Physical Structures: Level/graded soil bunds, stone bunds, Fanya Juu terraces (throwing soil upslope to form bench terraces over time), and cutoff drains.\n"
            "• Biological & Agronomic Measures: Contour plowing, Vetiver or Desho grass strips on bunds, agroforestry, cover cropping, minimum tillage, and surface mulching."
        ),
        "category": "Horticulture",
        "tags": "soil water conservation fanya juu bunds terraces erosion contour",
    },
    {
        "question": "Compare drip irrigation and furrow irrigation scheduling",
        "answer": (
            "• Drip Irrigation: Delivers water slowly near the root zone at 85–95% application efficiency, minimizes evaporation and foliar fungal diseases, and enables precise fertigation—ideal for high-value greenhouse & orchard crops.\n"
            "• Furrow Irrigation: Channels water between crop ridges (50–65% efficiency); low capital cost, suited to row crops like onion, tomato, and maize on gentle slopes (<2%).\n"
            "• Scheduling Formula: Crop Water Requirement ETc = ETo × Kc; Net Irrigation = ETc - Effective Rainfall."
        ),
        "category": "Horticulture",
        "tags": "drip furrow irrigation scheduling etc eto kc fertigation efficiency",
    },
    {
        "question": "Explain plant propagation methods grafting budding and tissue culture",
        "answer": (
            "• Grafting (Cleft, Whip-and-Tongue, Side-veneer): Joins a desirable scion shoot onto a hardy rootstock, aligning the vascular cambium layers tightly.\n"
            "• Budding (T-budding, Patch budding): Uses a single vegetative bud as the scion (popular in citrus and rose).\n"
            "• Tissue Culture (Micropropagation): Grows sterile explants on nutrient agar (MS medium + auxins/cytokinins) in vitro to rapidly mass-produce uniform, virus-free planting material (e.g., banana, enset, potato)."
        ),
        "category": "Horticulture",
        "tags": "plant propagation grafting budding tissue culture micropropagation cambium",
    },
    {
        "question": "What are key management factors in greenhouse protected cultivation?",
        "answer": (
            "Greenhouse management optimizes microclimate for year-round high-yield horticulture:\n"
            "• Temperature & Ventilation: Natural roof/side vents + shade nets (30–50%) prevent heat stress (>32°C causes pollen sterility in tomato).\n"
            "• Relative Humidity: Maintain 60–75% to support pollination while avoiding Botrytis/powdery mildew.\n"
            "• Fertigation & Sanitation: Automated drip fertigation monitoring EC (electrical conductivity) and pH (5.5–6.5), insect-proof 40–50 mesh screens, and footbaths."
        ),
        "category": "Horticulture",
        "tags": "greenhouse protected cultivation ventilation fertigation ec ph humidity",
    },
    {
        "question": "Explain climacteric vs non-climacteric fruits and postharvest cold chain handling",
        "answer": (
            "• Climacteric Fruits (banana, mango, avocado, tomato, papaya): Show a sharp spike in respiration and ethylene production during ripening; can be harvested mature-green and ripened off-tree.\n"
            "• Non-Climacteric Fruits (citrus, grape, pineapple, strawberry): Ripen gradually without an ethylene surge and must be harvested at eating maturity.\n"
            "• Postharvest Handling: Harvest during cool morning hours, pre-cool rapidly (hydro-cooling/forced air) to slow respiration (Q10 rule), avoid chilling injury in tropical fruits (<10–13°C), and use sanitized ventilated crates."
        ),
        "category": "Horticulture",
        "tags": "postharvest climacteric ethylene cold chain respiration chilling injury",
    },

    # =========================================================================
    # COMPUTER SCIENCE: CORE THEORY, DATA STRUCTURES, ALGORITHMS & OS
    # =========================================================================
    {
        "question": "Compare arrays vs linked lists in data structures",
        "answer": (
            "• Array: Contiguous memory block with O(1) random index access and great CPU cache locality, but fixed capacity (or O(n) resize/shift on middle insert/delete).\n"
            "• Linked List: Non-contiguous nodes storing data + pointer(s). Allows O(1) insertion/deletion when given a node reference, but requires O(n) sequential traversal and extra memory per pointer."
        ),
        "category": "Computer Science",
        "tags": "array linked list data structures memory complexity cache",
    },
    {
        "question": "Explain binary search trees AVL trees and B-Trees",
        "answer": (
            "• Binary Search Tree (BST): Left subtree < node < right subtree; average O(log n) search, degrades to O(n) if unbalanced.\n"
            "• AVL Tree: Self-balancing BST keeping height difference (balance factor) within {-1, 0, +1} via single/double rotations, guaranteeing O(log n) lookup.\n"
            "• B-Tree / B+ Tree: Multi-way balanced search tree optimized for disk/SSD block I/O; used internally by SQLite, PostgreSQL, and filesystems for database indexes."
        ),
        "category": "Computer Science",
        "tags": "bst avl b-tree binary search tree balancing database index",
    },
    {
        "question": "How do hash tables work and how are collisions resolved?",
        "answer": (
            "A Hash Table maps keys to bucket indices via `index = hash(key) % capacity`, giving O(1) average lookup, insert, and delete.\n"
            "Collisions (two keys hashing to the same bucket) are resolved via:\n"
            "1) Separate Chaining: Each bucket holds a linked list or small tree of colliding entries.\n"
            "2) Open Addressing (Linear Probing, Quadratic Probing, Double Hashing): Probes subsequent slots in the array until an empty slot is found.\n"
            "When load factor (n/capacity) exceeds ~0.75, the table resizes and rehashes."
        ),
        "category": "Computer Science",
        "tags": "hash table hashmap collision chaining probing load factor",
    },
    {
        "question": "Explain the four pillars of Object Oriented Programming OOP",
        "answer": (
            "The 4 OOP principles:\n"
            "1) Encapsulation: Bundling data and methods inside a class while hiding internal state behind access modifiers.\n"
            "2) Abstraction: Exposing essential interfaces while hiding implementation complexity.\n"
            "3) Inheritance: Creating specialized subclasses that reuse and extend behavior from a parent class.\n"
            "4) Polymorphism: Allowing one interface or superclass reference to execute different concrete behaviors at runtime (method overriding) or compile time (overloading)."
        ),
        "category": "Computer Science",
        "tags": "oop encapsulation abstraction inheritance polymorphism classes",
    },
    {
        "question": "What is the difference between a process and a thread in operating systems?",
        "answer": (
            "• Process: An independent executing program with its own isolated virtual address space, file descriptors, and PCB; inter-process communication (IPC) requires pipes, sockets, or shared memory.\n"
            "• Thread: The smallest unit of CPU scheduling inside a process. Threads within the same process share code, heap memory, and open files, while each thread keeps its own stack and CPU registers—making context switching faster, but requiring synchronization (mutexes/semaphores) to avoid race conditions."
        ),
        "category": "Computer Science",
        "tags": "process thread operating system os concurrency memory context switch",
    },
    {
        "question": "What are the four Coffman conditions for deadlock in OS?",
        "answer": (
            "Deadlock occurs only when all 4 Coffman conditions hold simultaneously:\n"
            "1) Mutual Exclusion: At least one resource is non-shareable.\n"
            "2) Hold and Wait: A process holds at least one resource while waiting for another.\n"
            "3) No Preemption: Resources cannot be forcibly taken away.\n"
            "4) Circular Wait: A closed cycle of processes exists where each waits for a resource held by the next.\n"
            "Breaking any one condition prevents deadlock."
        ),
        "category": "Computer Science",
        "tags": "deadlock coffman conditions mutual exclusion circular wait os",
    },
    {
        "question": "Explain Linux file permissions and chmod numeric notation",
        "answer": (
            "Linux permissions define Read (r = 4), Write (w = 2), and Execute (x = 1) for three classes: Owner (u), Group (g), and Others (o).\n"
            "• `chmod 755 script.sh` → Owner: 4+2+1=7 (`rwx`), Group: 4+1=5 (`r-x`), Others: 4+1=5 (`r-x`).\n"
            "• `chmod 644 notes.txt` → Owner: `rw-`, Group: `r--`, Others: `r--`.\n"
            "• `chmod 600 id_rsa` → Owner read/write only (private SSH keys)."
        ),
        "category": "Computer Science",
        "tags": "linux permissions chmod rwx 755 644 operating system",
    },
    {
        "question": "Explain De Morgan laws and discrete mathematics logic gates",
        "answer": (
            "De Morgan's Laws relate logical negation, AND, and OR:\n"
            "• `NOT (A AND B) ≡ (NOT A) OR (NOT B)`  →  `!(A && B) == (!A || !B)`\n"
            "• `NOT (A OR B) ≡ (NOT A) AND (NOT B)`  →  `!(A || B) == (!A && !B)`\n"
            "In digital logic, NAND and NOR gates are universal gates because any Boolean function (AND, OR, NOT, XOR) can be constructed from them alone."
        ),
        "category": "Computer Science",
        "tags": "discrete math de morgan laws boolean logic gates nand nor",
    },

    # =========================================================================
    # COMPUTER SCIENCE: NETWORKING & SECURITY
    # =========================================================================
    {
        "question": "Explain the 7 layers of the OSI model vs TCP IP model",
        "answer": (
            "OSI 7 Layers (top to bottom):\n"
            "7. Application (HTTP, DNS, SMTP) | 6. Presentation (TLS encryption, JSON/UTF-8) | 5. Session (dialog control)\n"
            "4. Transport (TCP/UDP, ports) | 3. Network (IP routing, ICMP) | 2. Data Link (MAC, Ethernet, switches) | 1. Physical (cables, Wi-Fi radio signals).\n"
            "The practical TCP/IP 4-layer model combines layers 5–7 into Application, keeps Transport and Internet (Network), and merges layers 1–2 into Link/Network Access."
        ),
        "category": "Computer Science",
        "tags": "osi model tcp ip 7 layers networking protocol",
    },
    {
        "question": "How does the TCP 3-way handshake work vs UDP?",
        "answer": (
            "• TCP (Connection-oriented, reliable, ordered): Establishes a connection via 3-way handshake: Client sends `SYN` → Server replies `SYN-ACK` → Client sends `ACK`. Guarantees delivery with sequence numbers, ACKs, and congestion control.\n"
            "• UDP (Connectionless, low-latency): Sends datagrams immediately without handshakes or retransmission—ideal for DNS queries, VoIP, video streaming, and online gaming."
        ),
        "category": "Computer Science",
        "tags": "tcp udp 3 way handshake syn ack networking transport",
    },
    {
        "question": "Explain DNS resolution and DHCP DORA process",
        "answer": (
            "• DNS (Domain Name System, Port 53): Translates human hostnames (e.g., `aau.edu.et`) into IP addresses via recursive resolver → Root server → TLD (`.et`/`.com`) → Authoritative nameserver.\n"
            "• DHCP (Dynamic Host Configuration Protocol, Ports 67/68): Automatically assigns IP, subnet mask, gateway, and DNS using the 4-step **DORA** cycle: **D**iscover → **O**ffer → **R**equest → **A**cknowledge."
        ),
        "category": "Computer Science",
        "tags": "dns dhcp dora ip resolution port 53 networking",
    },
    {
        "question": "Compare HTTP vs HTTPS and TLS encryption",
        "answer": (
            "• HTTP (Port 80): Transmits web requests and responses in plaintext, vulnerable to eavesdropping and tampering.\n"
            "• HTTPS (Port 443): Wraps HTTP inside **TLS** (Transport Layer Security). During the TLS handshake, the server proves identity via an X.509 digital certificate signed by a CA, uses asymmetric cryptography (ECDHE/RSA) to securely agree on ephemeral session keys, and then encrypts traffic rapidly with symmetric AEAD ciphers (AES-GCM or ChaCha20-Poly1305)."
        ),
        "category": "Computer Science",
        "tags": "http https tls ssl certificate encryption security",
    },
    {
        "question": "Compare hashing vs symmetric encryption vs asymmetric encryption",
        "answer": (
            "• Hashing (SHA-256, Argon2): One-way fixed-length digest used for integrity checks and password storage (cannot be reversed).\n"
            "• Symmetric Encryption (AES-256, ChaCha20): Uses the same shared secret key to encrypt and decrypt; ultra-fast for bulk data.\n"
            "• Asymmetric Encryption (RSA, ECC/Ed25519): Uses a public key to encrypt/verify and a mathematically linked private key to decrypt/sign—solving key distribution and digital signatures."
        ),
        "category": "Computer Science",
        "tags": "cryptography hashing sha256 aes rsa symmetric asymmetric security",
    },
    {
        "question": "What are firewall fundamentals and ethical network scanning concepts?",
        "answer": (
            "• Firewalls: Filter network traffic by IP, port, protocol (stateless packet filtering), connection state (stateful inspection), or Layer-7 signatures (WAF/NGFW).\n"
            "• Ethical Security & Scanning: Authorized penetration testing begins with reconnaissance and port/service discovery (e.g., Nmap TCP SYN `-sS` or version `-sV` scans) solely on permitted targets to uncover open ports, unpatched services, and OWASP Top 10 risks (SQL injection, XSS, broken access control) before attackers can exploit them."
        ),
        "category": "Computer Science",
        "tags": "firewall ethical hacking nmap network scanning owasp cybersecurity",
    },

    # =========================================================================
    # COMPUTER SCIENCE: DATABASES & SOFTWARE ENGINEERING
    # =========================================================================
    {
        "question": "Explain database normalization 1NF 2NF and 3NF with examples",
        "answer": (
            "Normalization reduces redundancy and update anomalies in relational databases:\n"
            "• 1NF (First Normal Form): Atomic column values only (no repeating groups or comma-separated lists) and a primary key.\n"
            "• 2NF (Second Normal Form): Must be in 1NF and every non-key attribute must depend on the ENTIRE primary key (eliminates partial dependencies on composite keys).\n"
            "• 3NF (Third Normal Form): Must be in 2NF and have NO transitive dependencies (non-key attributes depend ONLY on the primary key, not on another non-key column)."
        ),
        "category": "Computer Science",
        "tags": "database normalization 1nf 2nf 3nf bcnf sql relational",
    },
    {
        "question": "What are ACID properties in relational database transactions?",
        "answer": (
            "ACID guarantees reliable database transactions (e.g., in SQLite and PostgreSQL):\n"
            "• Atomicity: All operations in a transaction succeed together or roll back completely ('all or nothing').\n"
            "• Consistency: Every committed transaction preserves all schema constraints, foreign keys, and invariants.\n"
            "• Isolation: Concurrent transactions do not corrupt each other's intermediate states.\n"
            "• Durability: Once committed, data survives power loss or crashes via write-ahead logging (WAL)."
        ),
        "category": "Computer Science",
        "tags": "acid atomicity consistency isolation durability database transaction sqlite",
    },
    {
        "question": "Explain SQL JOIN types INNER LEFT RIGHT and FULL JOIN",
        "answer": (
            "• `INNER JOIN`: Returns only rows where the join key matches in both tables.\n"
            "• `LEFT JOIN` (`LEFT OUTER JOIN`): Returns all rows from the left table and matching rows from the right table (or `NULL` if no match).\n"
            "• `RIGHT JOIN`: Returns all rows from the right table and matching rows from the left.\n"
            "• `FULL OUTER JOIN`: Returns all rows from both tables, filling unmatched sides with `NULL`."
        ),
        "category": "Computer Science",
        "tags": "sql join inner left right outer query database",
    },
    {
        "question": "Compare SDLC models Waterfall vs Agile Scrum",
        "answer": (
            "• Waterfall: Sequential phases (Requirements → Design → Implementation → Testing → Deployment). Best when requirements are fixed, regulatory, or hardware-bound.\n"
            "• Agile / Scrum: Iterative 1–4 week sprints delivering working increments, daily standups, sprint reviews, and retrospectives. Adapts smoothly to evolving user needs and continuous feedback."
        ),
        "category": "Computer Science",
        "tags": "sdlc waterfall agile scrum software engineering methodology",
    },
    {
        "question": "Explain Git version control workflow branch commit merge and rebase",
        "answer": (
            "Essential Git commands:\n"
            "• `git status` / `git add <file>` / `git commit -m \"msg\"`: Stage and snapshot changes locally.\n"
            "• `git checkout -b feature/xyz` (or `git switch -c`): Create an isolated feature branch.\n"
            "• `git merge`: Joins branch histories with a merge commit, preserving full branching history.\n"
            "• `git rebase main`: Replays feature commits cleanly on top of the latest `main` for a linear history (never rebase shared public branches!)."
        ),
        "category": "Computer Science",
        "tags": "git version control branch commit merge rebase workflow",
    },
]
