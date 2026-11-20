# SM printer squeegee range. Model column keeps the ORIGINAL printer-brand model (Jason 2026-11-19).
# CNY = Youzuo (supplier, never shown) shop-search card price 2026-11-19 = lowest variant of each listing.
# USD = round(CNY x 2 / 6.6). Item ids kept only here for traceability.
ROWS = [
 # group, printer brand, original model / fit, product, configuration, CNY, item id
 ("A","DEK","DEK","Metal squeegee assembly","Aluminium holder + stainless blade, fixed end dams; 150-750 mm",180,"38890346796"),
 ("A","DEK","DEK","Glue (adhesive) squeegee assembly","Holder + rubber blade for red glue printing",380,"526270588411"),
 ("A","MPM","MPM UP2000","Metal squeegee assembly","Holder + stainless blade",200,"38919560788"),
 ("A","MPM","MPM 125 / Momentum","Metal squeegee assembly","Holder + stainless blade",25,"38919280235"),
 ("A","GKG","GKG (G2 / G3 / G5 / GSE)","Metal squeegee assembly","Holder + stainless blade, fixed or elastic end dams",180,"40704871598"),
 ("A","GKG / Desen","GKG / Desen","Glue (adhesive) squeegee assembly","Holder + rubber blade for red glue",570,"39512106063"),
 ("A","GKG / Desen / DEK","GKG / Desen / DEK","Paste-saving squeegee (elastic end dams)","Elastic end dams keep paste inside the print area",80,"520231076813"),
 ("A","Desen","Desen","Metal squeegee assembly","Holder + stainless blade",180,"38890970264"),
 ("A","Hetian Gude","Hetian Gude","Metal squeegee assembly","Holder + stainless blade",180,"42058988864"),
 ("A","Zhengshi","Zhengshi (L8 / L12 / L15)","Metal squeegee assembly","Holder + stainless blade",450,"596218152570"),
 ("A","Panasonic","Panasonic SP28 / SP60","Squeegee assembly","Holder + blade",550,"38694803808"),
 ("A","Panasonic","Panasonic SP18 / SPG / SPD","Squeegee assembly","Holder + blade",35,"38889470469"),
 ("A","Yamaha","Yamaha YGP / YCP / YSP","Squeegee assembly","Holder + blade",1200,"618569327471"),
 ("A","Yamaha","Yamaha YVP","Squeegee assembly","Holder + blade",450,"525195304832"),
 ("A","EKRA","EKRA","Squeegee assembly","Holder + stainless blade",450,"38887463353"),
 ("A","EKRA","EKRA (new type)","Squeegee assembly","Holder + stainless blade",500,"694439159777"),
 ("A","Nitto","Nitto (semi / fully automatic)","Squeegee assembly","Holder + blade; holder height per printer",450,"38886887843"),
 ("B","GKG / DEK / MPM / Desen","Universal","Stainless steel blade","0.3 mm standard; 0.2 / 0.25 / 0.4 / 0.5 mm on request",25,"550450955046"),
 ("B","MPM","MPM 125 / Momentum","Stainless steel blade","Replacement blade",25,"38682606131"),
 ("B","MPM","MPM UP2000","Stainless steel blade","Replacement blade",17,"38692963103"),
 ("B","EKRA","EKRA","Stainless steel blade","Replacement blade",25,"38710916219"),
 ("B","Panasonic","Panasonic SP18 / SP28","Blade","Replacement blade",30,"694828570197"),
 ("B","Universal","Universal","Rubber glue blade, bevel edge","For glue / adhesive printing",60,"38714701193"),
 ("B","Universal","Universal","Rubber glue blade, flat edge","For glue / adhesive printing",60,"38693151597"),
 ("B","Universal","Universal","Rubber glue blade, pointed edge","For glue / adhesive printing",60,"38693507144"),
 ("B","Universal","Universal","M5 holder screw / nut","Spare fixing",10,"694175960906"),
 ("C","Universal","DEK / MPM / GKG etc.","Squeegee storage cabinet","Holds squeegee sets in fixed positions",1600,"635920750403"),
 ("C","Panasonic / Fuji / Yamaha","Panasonic / Fuji GPX / Yamaha / MPM","Squeegee storage cabinet","Brand-specific slots",1600,"902098762558"),
 ("C","Custom","Custom","Squeegee storage cabinet, custom size","Built to your squeegee count and lengths",2998,"1094583318540"),
]
# DEK SQA part numbers (blade length) - from SQA listing (other shop), used for model table only
DEK_SQA = [("SQA300",170),("SQA301",200),("SQA302",250),("SQA303",300),("SQA304",350),("SQA305",400),
           ("SQA306",440),("SQA307",483),("SQA308",510),("SQA309",535),("SQA489",580),("SQA478",610)]
usd = lambda c: int(round(c*2/6.6))
GROUPS = {"A":"Squeegee assemblies (holder + blade, per printer brand)","B":"Blades and spares","C":"Squeegee storage"}
