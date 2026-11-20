import json, sys
CT = "Send it to info@smthelp.com or WhatsApp +86 136 0256 2576, or use the form on this page."
B = [
[
"A buyer orders 'wiping paper 410 x 300' for a printer that has always run 300 mm rolls, and the delivery does not fit the roll holder.",
"Wiping roll sizes are written as three numbers, and they are easy to read the wrong way. The first number is the core (tube) length, the second the paper width, the third the roll length. Read the first number as the paper width, or the second as the roll diameter, and the order looks right on paper and wrong at the printer.",
"Use one convention everywhere: core length x paper width x roll length. The core length is set by the printer - 410 mm for GKG and Desen, 530 mm for DEK, 455 mm for MPM, 350 mm for the Panasonic paper-tube roll. The paper width is set by the stencil area you need to clean. The roll length is usually 10 m, and a 10 m roll is only about 50 mm across.",
"Southern Machinery lists every roll in that order and codes it the same way: SM-WP-410-300-10-X is a 410 mm core, 300 mm paper, 10 m roll with a cross-slot core. The size selector on this page goes from printer brand to core length, paper widths and core opening.",
"Write the full size on the label of each printer's spare-roll shelf and on the purchase record. When the next order is placed, it is copied, not re-measured.",
"Send us the printer model and the three numbers from your current roll - or a photo of it next to a ruler. " + CT
],
[
"A new roll has the right length and width, slides onto the shaft, and the paper does not advance during the wipe.",
"The core end is the part that engages the printer's drive, and printers use different ones. GKG rolls have a cross slot at both ends, MPM cores have 12 inner grooves, DEK cores a straight slot, Panasonic, Yamaha and Hitachi use paper tubes of 38, 25.5 and 30 mm. A roll with the wrong core end either does not mount or slips on the shaft.",
"Check the opening before the size. Look at the end of the old core and name it: cross slot, straight slot, 12 grooves, paper tube or plain tube. Note the inner diameter too - 20 mm for GKG and DEK, 19.5 mm for MPM, 8 mm for MINAMI. Where your printer's rolls have been sold with more than one opening, as for Desen and DEK, a photo settles it.",
"Southern Machinery supplies rolls with cross slot, straight slot, 12-groove and paper-tube cores, and the code shows the opening: X, S, G or P. If the printer is not in our size table, we match the core from your photo and measurements.",
"Keep one photo of each printer's core end with the spare-roll record. It answers the question for every later order.",
"Send a photo of your old core end with the printer model and roll size. " + CT
],
[
"The right roll arrives, the operator mounts it, and the paper comes off the wrong side of the roll.",
"Roll direction - whether the paper leaves the roll over the top or from underneath when the roll sits in the printer - is rarely written down. Size lists do not show it either, yet the market sellers ask buyers to confirm it before ordering, because a roll wound the other way does not feed as the printer expects.",
"Record it once per printer. Before you take an old roll out, photograph it in place with the paper path visible, or mark the side the paper leaves on the core end. Send that photo with the first order and keep it with the printer's records.",
"Southern Machinery asks for the roll direction with every new printer and confirms it with you before the order is packed. A photo is enough; no drawing is needed.",
"Add the photo to the changeover instructions at the printer. The next operator mounts the roll correctly the first time.",
"Send us the photo of your old roll as it sits in the printer, with model and size. " + CT
],
[
"After a wipe the stencil underside looks clean, and the AOI still finds small fibres on pads of the next board.",
"A wipe that leaves fibres behind trades one defect for another. Loose fibres are carried into apertures and onto pads, where they disturb paste release and solder joints. Paper that sheds lint is therefore a print-quality problem, not only a housekeeping one.",
"Judge wiping paper by what it leaves behind as well as by what it removes. Check the stencil underside after a test wipe under good light, and look for fibres on pads in the first board after the wipe.",
"Southern Machinery wiping paper is a two-layer hydroentangled web of long-fibre wood pulp and polyester with a near lint-free surface. The pulp side absorbs, the polyester side keeps the web together, and the rolls are packed against dust until use.",
"Make the test wipe part of every new roll batch or new supplier: one dry wipe, one wet wipe, one look at the underside and the first board.",
"Tell us your printer and the cleaning mode you run. " + CT
],
[
"A line buys the widest roll that fits the printer, because wider sounds safer, and uses more paper than it needs every shift.",
"Paper width does not have to match the core length. For each core length there is a range of widths - 200 to 400 mm on a 410 mm GKG core, 200 to 510 mm on a 530 mm DEK core. A roll narrower than the print area leaves residue at the edges; a roll much wider than it cleans stencil that never prints.",
"Choose the width from the stencil: the print area of your largest regular job plus a margin. If boards vary widely, standardise on two widths per printer rather than one width for everything.",
"Southern Machinery offers each core length in the market's standard widths, for example 200, 250, 300, 350, 380 and 400 mm on 410 mm cores, and makes custom widths on request. The size selector lists the widths per printer brand.",
"Review the width when a new product family arrives at the printer. A wider board may need a wider roll; a smaller one may let you save paper.",
"Send us your printer model and the print area of your largest stencil. " + CT
],
[
"Halfway through a wet wipe the paper tears, the printer stops and the operator rethreads the roll while boards wait.",
"Under-stencil cleaning often runs wet: solvent is sprayed onto the paper before it is pressed against the stencil. Paper that is strong dry and weak wet will tear at exactly that moment, and the partial wipe leaves residue behind.",
"Ask two questions of any wiping paper: does it absorb the solvent and paste quickly, and does it stay intact when soaked? Test it with your own solvent on your own printer before switching a whole line.",
"Southern Machinery wiping paper combines natural wood pulp, which soaks up water and oil, with polyester, which gives it tensile strength and flexibility. It is used dry or with stencil cleaning solvents.",
"Keep the test record: solvent, wipe mode, result. When the solvent or the paste changes, repeat the test.",
"Tell us the printer and the solvent you use. " + CT
],
[
"The printer stops for a cleaning error, and the store room has rolls - for a different printer.",
"Wiping roll usage is predictable. It follows prints per day, the cleaning interval and the paper advance per wipe, all of which are settings in the printer. Yet rolls are often reordered only when the last one is mounted.",
"Calculate it once per printer: prints per day divided by prints between wipes gives wipes per day; multiplied by the paper per wipe and the working days it gives metres per month; divided by the roll length it gives rolls per month. The planner on this page does the arithmetic with your own settings.",
"Southern Machinery supplies rolls for every printer on the line from one source, sized and labelled by printer, so stock can be kept per printer rather than per guess.",
"Set a minimum stock of one spare roll per printer plus the monthly usage, and review it when cleaning settings change.",
"Send us your printer list and monthly usage, and we quote the set. " + CT
],
[
"An enquiry says 'SMT wiping paper, 20 rolls' and starts a week of questions before a quote is possible.",
"A wiping roll is defined by more than its name. Without the printer model, core length, paper width, roll length, core opening and roll direction, any supplier has to guess or ask, and a guess that is wrong costs a delivery.",
"Send five things with the first enquiry: printer brand and model; core length; paper width; core opening (or a photo of the core end); and roll direction (a photo of the old roll in place). Add quantity per printer.",
"Southern Machinery checks these five points against its size table and confirms them in writing with the quotation, so the roll that arrives is the roll that fits.",
"Keep the confirmed specification as your reference for repeat orders: one line per printer, with the SM code.",
"Send the five details and the quantity. " + CT
],
]
if __name__ == "__main__":
    assert len(B) == 8 and all(len(x) == 6 for x in B)
    json.dump(B, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("blogs", len(B))
