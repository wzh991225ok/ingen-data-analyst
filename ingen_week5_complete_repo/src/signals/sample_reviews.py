"""Labelled SAMPLE review corpus (synthetic, illustrative) for the VoC module.

These are NOT real customer reviews. They are realistic-but-synthetic samples that let
the topic-modelling pipeline run end-to-end. To analyse real voice-of-customer data,
drop a real export at data/week05/reviews_<vertical>.csv with a `text` column; the
module will use that instead and the manifest will record mode='file'.
"""

SAMPLE_REVIEWS = {
"eldercare": [
 "The companion robot is great for reminders but the battery drains by midday and it stops responding.",
 "My mother loves talking to it, though the voice recognition fails when she speaks softly.",
 "Setup was confusing and the app keeps disconnecting from the home wifi.",
 "Very helpful for medication reminders, but it is too expensive for what it does.",
 "It fell off the table and broke; build quality feels fragile for elderly use.",
 "Good for video calls with family, however the screen is small and hard to see.",
 "The fall-detection feature gives false alarms and is unreliable at night.",
 "Lovely idea but customer support was slow and we had to return one unit.",
 "It reminds my dad to drink water which is wonderful, wish it moved between rooms.",
 "Wheels get stuck on carpet and it cannot navigate the hallway on its own.",
 "Reassuring to have check-ins, but subscription cost on top of the device is too high.",
 "Speaker volume is too low for hard-of-hearing users, a real accessibility miss.",
],
"education": [
 "Kids love building with it, but the curriculum content runs out quickly.",
 "Great STEM tool, however the app crashes during multi-student classroom sessions.",
 "Setup across 30 tablets is painful and the bluetooth pairing keeps dropping.",
 "Engaging for coding lessons, but it is expensive per classroom and licensing is unclear.",
 "Durable enough for younger kids, though parts are easy to lose.",
 "Teacher dashboard is confusing and reporting on student progress is limited.",
 "Motivates reluctant learners, but it needs constant wifi and lags on our network.",
 "Good for special-needs students, wish there were more languages supported.",
 "Battery life is short so we cannot get through a full school day.",
 "Lots of potential but firmware updates break existing lesson plans.",
 "Customer service was slow when two units stopped charging.",
 "Fun but the noise level in a classroom of these is distracting.",
],
"indoor_security": [
 "Cuts our guard costs but the robot gets stuck at thresholds and needs help.",
 "Night patrol coverage is good, however the camera struggles in low light.",
 "Integration with our access-control system was difficult and poorly documented.",
 "Reliable indoors but the monthly service fee is very expensive.",
 "False intruder alerts at night are frequent and annoying for the team.",
 "Elevator integration fails so it cannot cover multiple floors on its own.",
 "Great deterrent presence, but battery requires frequent docking and downtime.",
 "Mapping the building took days and re-mapping after layout changes is painful.",
 "Useful logs and reports, though the dashboard is slow and clunky.",
 "Wheels slip on polished floors and navigation is unreliable in crowds.",
 "Support response was slow when the sensor module failed.",
 "Good ROI versus a human guard, but upfront deployment cost is high.",
],
"outdoor_patrol": [
 "Covers the perimeter well, but rain and mud cause it to get stuck.",
 "Good for large sites, however GPS drifts near buildings and it loses its route.",
 "Thermal camera is useful at night but the battery dies on long patrols.",
 "Reduced our patrol headcount, yet the service contract is expensive.",
 "Rugged build, though it struggles on gravel and steep ramps.",
 "Connectivity drops in far corners of the yard and it stops reporting.",
 "Useful alerts, but too many false positives from animals and shadows.",
 "Charging downtime means we still need a backup human patrol.",
 "Setup of geofences was confusing and documentation was thin.",
 "Handles weather better than expected, but maintenance is frequent.",
 "Support was slow to ship a replacement wheel module.",
 "Great visibility deterrent, however upfront cost is hard to justify for small sites.",
],
"humanoid": [
 "Impressive demo but in practice it is slow and frequently needs a human to reset it.",
 "Can pick and place, however it struggles with anything outside a narrow set of tasks.",
 "Battery runtime is short and swapping is awkward on the line.",
 "Extremely expensive and the ROI is unclear for our facility right now.",
 "Hardware feels solid, but the software is buggy and updates break calibration.",
 "Promising for repetitive tasks, yet setup and safety fencing took weeks.",
 "Grip is unreliable on irregular parts and it drops items.",
 "Support is responsive but spare parts have long lead times.",
 "Good for lifting, though it is noisy and overheats during long shifts.",
 "Still early; needs constant supervision so labour savings are limited so far.",
 "Integration with our MES was difficult and poorly documented.",
 "Exciting technology but reliability is not there for 24/7 production yet.",
],
}


# Additional labelled SAMPLE reviews (synthetic) to support 5 themes x >=3 examples per vertical.
_EXTRA = {'eldercare': ['The reminder feature is reliable but it cannot move between rooms which limits usefulness.', 'Charging dock is finicky and some mornings the unit is dead.', 'Voice prompts are clear, yet it mishears my mother when the TV is on.', 'We loved the check-in calls but had to return it after the screen cracked.', 'Navigation around furniture is poor and it bumps into table legs.', 'Subscription pricing is steep for a fixed-position device.', 'Setup needed my grandson; the wifi pairing kept failing for elderly users.', 'Volume is too low for hard-of-hearing relatives, an accessibility gap.'], 'education': ['Pairing across a classroom set of tablets is unreliable and drops often.', 'Reporting in the teacher dashboard is thin and hard to interpret.', 'Battery does not last a full school day so lessons get interrupted.', 'Firmware updates broke our saved lesson plans last term.', 'Great engagement but licensing cost per classroom is unclear and high.', 'Noise from a room full of units is distracting for students.', 'Limited language support restricts use for ESL students.', 'Durable build for kids, though small parts are easily lost.'], 'indoor_security': ['Elevator integration fails so it cannot patrol multiple floors alone.', "Frequent false intruder alerts overnight waste the team's time.", 'Re-mapping after a floor layout change is slow and painful.', 'Monthly service fee is expensive relative to the coverage.', 'Camera struggles in low light despite good daytime performance.', 'Wheels slip on polished floors and it stalls in crowded lobbies.', 'Dashboard is slow and clunky when pulling incident logs.', 'Support was slow to replace a failed sensor module.'], 'outdoor_patrol': ['GPS drifts near tall buildings and the robot loses its patrol route.', 'Battery dies on long perimeter loops so we keep a backup patrol.', 'Too many false positives from animals and moving shadows at night.', 'Connectivity drops in far corners of the yard and reporting stops.', 'Rugged but it gets stuck in mud and on loose gravel after rain.', 'Geofence setup was confusing and documentation was thin.', 'Maintenance is frequent and a wheel module replacement took weeks.', 'Upfront cost is hard to justify for a small site.'], 'humanoid': ['Needs a human to reset it often, so labour savings are limited.', 'Grip is unreliable on irregular parts and it drops items.', 'Battery runtime is short and hot-swapping on the line is awkward.', 'Software is buggy and updates break calibration.', 'Safety fencing and setup took weeks before first use.', 'Integration with our MES was poorly documented and slow.', 'Overheats and is noisy during long continuous shifts.', 'Extremely expensive with unclear ROI for our plant today.']}
for _k,_v in _EXTRA.items():
    SAMPLE_REVIEWS[_k] = SAMPLE_REVIEWS[_k] + _v
