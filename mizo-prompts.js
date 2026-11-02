// Adapted from Flaq AI's MIT-licensed templates. See assets/FLAQ-LICENSE.txt.
const mizoPrompts=[
  {
    "title": "Aizawl Rooftop Editorial",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/07-photography-and-editorial.md",
    "text": "Create a photorealistic 4:5 editorial portrait using the supplied person reference. A contemporary Mizo creator pauses on an Aizawl rooftop after rain, checking a camera. Use the supplied city photo for accurate skyline and building details. Eye-level 50mm perspective, cloudy daylight with one restrained cyan reflection, natural skin and worn technical streetwear. Preserve identity and realistic hands. No costume styling, invented signage or beauty-filter skin.",
    "category": "image"
  },
  {
    "title": "Hill-City Evening Walk",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/07-photography-and-editorial.md",
    "text": "Create a candid 3:2 street photograph inspired by a present-day Aizawl evening. Use the supplied street reference for slopes, buildings and road layout. Follow one person in everyday clothing walking past small shops after rain, warm window light, cool cloud cover, natural colour, 35mm documentary framing. Keep cars, pedestrians and road width plausible. No staged traditional costume, fantasy landmarks or invented readable shop signs.",
    "category": "image"
  },
  {
    "title": "Aizawl Cafe Weekly Special",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/10-local-business-campaigns.md",
    "text": "Design a 4:5 weekly-special post for [CAFE NAME] in Aizawl. Use the uploaded dish photograph without changing its ingredients or portion. Soft side-window lighting, charcoal tabletop, restrained cyan accent and generous negative space. Render only this supplied text: [DISH NAME], [VERIFIED PRICE], [AVAILABILITY], [CALL TO ACTION]. Keep all text legible on a phone. No invented discounts, business details, toppings or cultural props.",
    "category": "image"
  },
  {
    "title": "Hill-City Studio Opening",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/10-local-business-campaigns.md",
    "text": "Create a contemporary 4:5 opening announcement for [STUDIO NAME], a [BUSINESS TYPE] in [VERIFIED AIZAWL AREA]. Use the supplied storefront photo faithfully. Build a clean graphic motif from the stepped hillside silhouette, with black, off-white and one magenta accent. Use only the approved headline, business name, opening hours and address supplied by the owner. No fake reviews, QR codes, landmarks or decorative traditional motifs.",
    "category": "image"
  },
  {
    "title": "KhiangteVillain Character Bible",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/06-characters-and-storytelling.md",
    "text": "Use the uploaded official KhiangteVillain artwork as the identity anchor. Create a clean 3:2 character reference sheet showing front, three-quarter, side and back views of the hooded creator, plus mask and jacket details. Preserve the cyan eye shape, dotted mask, hood silhouette, black outerwear construction and cyan/magenta palette across views. This is a design reference, not an aligned animation sprite sheet. Plain neutral background; no extra logos, words, costumes or invented face beneath the mask.",
    "category": "image"
  },
  {
    "title": "Monsoon Reel Storyboard",
    "source": "https://github.com/flaqai/awesome-nano-banana-prompts/blob/main/prompts/06-characters-and-storytelling.md",
    "text": "Create a black-and-white 16:9 contact sheet with exactly six numbered storyboard frames for a contemporary Aizawl rain-night reel. Use the supplied character and street references. Frames: hillside street wide; creator entering a cafe; wet camera strap detail; glance toward the window; view down the stepped street; final rooftop skyline. Maintain clothing, weather, light direction and street geometry. Use clear shot-size changes and simple movement arrows. No extra panels, dialogue, invented landmarks or costume changes.",
    "category": "image"
  }
];
prompts.unshift(...mizoPrompts);
render();
